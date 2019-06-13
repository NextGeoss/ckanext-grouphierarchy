import ckan.plugins as p
import ckan.model as model
from ckan.common import request, config

from ckanext.opensearch import config as opensearch_config


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
    group_list = config.get('ckan.featured_groups')

    groups = h.get_featured_groups(count=40)

    for group in groups:
        if group['name'] in group_list:
            parent_groups.append(group)

    return parent_groups


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


def get_group_collection_count(group):
    group_collections = []

    if group.extras is not None and group.extras.get('collections') is not None:
        collections = group.extras.get('collections')

        for collection in collections.split(", "):
            group_collections.append(collection)

    collections = []

    for collection_id in group_collections:
        item = collection_information(collection_id)
        collections.append(item)

    return len(collections)


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