import ckan.plugins as p
import ckan.model as model
import ckan.logic as logic
from ckan.common import request, config
import ckan.lib.helpers as h

from ckanext.opensearch import config as opensearch_config
from ckanext.nextgeoss import helpers as ng_helpers

import ast


def get_allowable_parent_groups(group_id):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = \
            group.groups_allowed_to_be_its_parent(type='group')
    else:
        allowable_parent_groups = model.Group.all(
            group_type='group')
    return allowable_parent_groups


def get_parent_groups():
    parent_groups = []
    group_list = config.get('ckan.featured_groups').split()

    groups = h.get_featured_groups(count=40)

    for group in groups:
        if group['name'] in group_list:
            parent_groups.append(group['name'])

    return parent_groups

def get_children_groups():
    group_list = model.Group.all(group_type='group')
    parent_group_names = get_parent_groups()
    children_groups = [group for group in group_list
                       if group.name not in parent_group_names]

    return children_groups

def is_include_children_selected(fields):
    include_children_selected = False
    if request.params.get('include_children'):
        include_children_selected = True
    return include_children_selected


def get_children_names(group_name):
    children = []

    group = model.Group.get(group_name)
    children =  model.Group.get_children_groups(group)

    groups = model.Group.all(group_type='group')

    for g in groups:
        if g.extras.get('secondary_parent') is not None:
            secondary_parent = list(g.extras.get('secondary_parent').split(', '))

            if str(group_name) in secondary_parent and g not in children:
                children.append(g)
    return children


def collection_information(collection_id=None):
    collections = opensearch_config.load_settings("collections_list")
    collection_items = collections.items()

    for collection in collection_items:
        if collection[0] == collection_id:
            return dict(collection[1])


def get_children_group_count(name):
    group = model.Group.get(name)

    children =  model.Group.get_children_groups(group)

    return len(children)


def get_topic_type_internal(groups):
    internal_topics = []

    for group in groups:
        if group.extras.get('topic_type') == 'internal':
            internal_topics.append(group)

    return internal_topics


def get_topic_type_external(groups):
    external_topics = []

    for group in groups:
        if group.extras.get('topic_type') == 'external':
            external_topics.append(group)

    return external_topics

def get_topic_collections(name):
    group_collections = []
    collections = []

    group = model.Group.get(name)
    if group.extras.get('collections'):
        group_collections = group.extras.get('collections').split(", ")

    for collection_id in group_collections:
        item = ng_helpers.collection_information(collection_id)
        if item:
            item['id'] = collection_id
            collections.append(item)

    return collections

def is_internal(group):
    group = model.Group.get(group['name'])
    return group.extras.get('topic_type') == 'internal'

def is_external(group):
    group = model.Group.get(group['name'])
    return group.extras.get('topic_type') == 'external'

def get_output_datasets(group):
    output_datasets = []
    group = model.Group.get(group['name'])
    group_packages = group.packages()
    for package in group_packages:
        extras = package.as_dict().get('extras', {})
        if extras.get('is_output') == 'true':
            output_datasets.append(package.as_dict())

    return output_datasets
