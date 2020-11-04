# -*- coding: utf-8; -*-
# This file is part of Superdesk.
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license
#
# Author  : administrator
# Creation: 2020-11-04 00:16

from superdesk.commands.data_updates import DataUpdate


class DataUpdate(DataUpdate):

    resource = 'content_templates'

    def forwards(self, mongodb_collection, mongodb_database):
        mongodb_collection.drop_index('user_1_template_name_1')

    def backwards(self, mongodb_collection, mongodb_database):
        pass
