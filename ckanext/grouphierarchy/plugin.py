import routes.mapper
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultGroupForm
from ckan.common import c, request
from ckanext.grouphierarchy import helpers


class GrouphierarchyPlugin(plugins.SingletonPlugin, DefaultGroupForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IGroupForm, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'grouphierarchy')

    # ITemplateHelpers
    def get_helpers(self):
        return {
        		'get_allowable_parent_groups': helpers.get_allowable_parent_groups,
                'is_include_children_selected': helpers.is_include_children_selected,
                'get_children_names': helpers.get_children_names,
                'get_children_group_count': helpers.get_children_group_count,
                'get_parent_groups': helpers.get_parent_groups,
                'get_children_groups': helpers.get_children_groups,
                'get_topic_type_internal': helpers.get_topic_type_internal,
                'get_topic_type_external': helpers.get_topic_type_external,
                'get_topic_collections': helpers.get_topic_collections,
                'is_internal': helpers.is_internal,
                'is_external': helpers.is_external,
                'get_group_show': helpers.get_group_show,
                'get_group_date': helpers.get_group_date,
                }

    # IGroupForm

    def group_types(self):
        return ('group',)

    def group_controller(self):
        return 'group'

    def setup_template_variables(self, context, data_dict):
        from pylons import tmpl_context as c

        group_id = data_dict.get('id')
        c.allowable_parent_groups = helpers.get_allowable_parent_groups(group_id)

    def before_map(self, map):
        package_controller = 'ckanext.grouphierarchy.controllers.package:GrouphierarchyPackageController'  # noqa: E501
        with routes.mapper.SubMapper(map, controller=package_controller) as m:
          m.connect('dataset_groups', '/dataset/groups/{id}', action='groups')
        return map
