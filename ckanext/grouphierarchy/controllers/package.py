# encoding: utf-8

import logging

import ckan.lib.base as base
import ckan.model as model
import ckan.logic as logic

from ckan.controllers.package import PackageController, _encode_params
from ckan.common import OrderedDict, _, json, request, c, response
import ckan.lib.helpers as h
from ckan.common import config
from ckanext.grouphierarchy import helpers


log = logging.getLogger(__name__)

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key


class GrouphierarchyPackageController(PackageController):
    def groups(self, id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj, 'use_cache': False}
        data_dict = {'id': id}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except (NotFound, NotAuthorized):
            abort(404, _('Dataset not found'))

        if request.method == 'POST':
            new_group = request.POST.get('group_added')
            if new_group:
                data_dict = {"id": new_group,
                             "object": id,
                             "object_type": 'package',
                             "capacity": 'public'}
                try:
                    get_action('member_create')(context, data_dict)
                except NotFound:
                    abort(404, _('Group not found'))

            removed_group = None
            for param in request.POST:
                if param.startswith('group_remove'):
                    removed_group = param.split('.')[-1]
                    break
            if removed_group:
                data_dict = {"id": removed_group,
                             "object": id,
                             "object_type": 'package'}

                try:
                    get_action('member_delete')(context, data_dict)
                except NotFound:
                    abort(404, _('Group not found'))
            h.redirect_to(controller='package', action='groups', id=id)

        context['is_member'] = True
        users_groups = get_action('group_list_authz')(context, data_dict)

        children_groups = helpers.get_children_groups()
        children_group_ids = [group.id for group in children_groups]
        children_user_groups = [group for group in users_groups
                                if group['id'] in children_group_ids]

        pkg_group_ids = set(group['id'] for group
                            in c.pkg_dict.get('groups', []))
        children_pkg_group_ids = [group.id for group in children_groups
                                  if group.id in pkg_group_ids]
        user_group_ids = set(group['id'] for group
                             in users_groups)

        c.group_dropdown = [[group['id'], group['display_name']]
                            for group in children_user_groups if
                            group['id'] not in children_pkg_group_ids]

        for group in c.pkg_dict.get('groups', []):
            group['user_member'] = (group['id'] in user_group_ids)

        return render('package/group_list.html',
                      {'dataset_type': dataset_type})
