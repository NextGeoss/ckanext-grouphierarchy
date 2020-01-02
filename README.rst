.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/NextGeoss/ckanext-grouphierarchy.svg?branch=master
    :target: https://travis-ci.org/NextGeoss/ckanext-grouphierarchy

.. image:: https://coveralls.io/repos/NextGeoss/ckanext-grouphierarchy/badge.svg
  :target: https://coveralls.io/r/NextGeoss/ckanext-grouphierarchy

.. image:: https://pypip.in/download/ckanext-grouphierarchy/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-grouphierarchy/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-grouphierarchy/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-grouphierarchy/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-grouphierarchy/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-grouphierarchy/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-grouphierarchy/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-grouphierarchy/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-grouphierarchy/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-grouphierarchy/
    :alt: License

=============
ckanext-grouphierarchy
=============
This extension adds functionality to creates subgroups within a group.

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-grouphierarchy:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-grouphierarchy Python package into your virtual environment::

     pip install ckanext-grouphierarchy

3. Add ``grouphierarchy`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

The plugin adds functionality the group create/edit form allowing you to assign the group to another parent group.

If the group should be assigned to multiple parent groups, you can specify the others by the following attribute the groups extras:

    secondary_parent: secondary_parent_group_id


You can also mark a group as `external` or `internal` by setting it in the extras:


    topic_type: external/internal


Depending on this attribute child groups will be displayed either in the parent's `External Services` section
or in the parent's `Internal Services` section.

If you also want to display the Data Collections associated with a certain group, you can add the list of collection ids to the extras:


    collections: list,of,collection,ids


------------------------
Development Installation
------------------------

To install ckanext-grouphierarchy for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/NextGeoss/ckanext-grouphierarchy.git
    cd ckanext-grouphierarchy
    python setup.py develop
    pip install -r dev-requirements.txt

