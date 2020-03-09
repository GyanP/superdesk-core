# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : GyanP
# Creation: 2020-03-09 12:19

from bson import ObjectId
from bson.errors import InvalidId
from superdesk import get_resource_service
from superdesk.vocabularies import is_related_content
from superdesk.commands.data_updates import DataUpdate


class DataUpdate(DataUpdate):

    resource = 'archive'

    def forwards(self, mongodb_collection, mongodb_database):
        related = list(get_resource_service('vocabularies').get(req=None, lookup={'field_type': 'related_content'}))
        archive_service = get_resource_service('archive')
        for resource in ('archive', 'published'):
            service = get_resource_service(resource)
            for item in mongodb_database[resource].find({'associations': {'$gt': {}}}):
                update = False
                associations = {}
                for key, val in item['associations'].items():
                    associations[key] = val
                    if val and is_related_content(key, related) and val.get('order', None) is None:
                        update = True
                        order = int(key.split('--')[1])
                        associations[key]['order'] = order
                if update:
                    try:
                        _id = ObjectId(item['_id'])
                    except InvalidId:
                        _id = item['_id']
                    service.system_update(_id, {'associations': associations}, item)

    def backwards(self, mongodb_collection, mongodb_database):
        raise NotImplementedError()
