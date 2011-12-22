from datetime import datetime
from dateutil.parser import parse as dt_parse

from django.contrib.auth.models import User

from celery.task import Task
from celery.registry import tasks

from subscribers.models import GroupSubscription
from user_groups.models import Group
from user_groups.importer.utils import parse_subs_from_csv

class ImportMembershipsTask(Task):

    def run(self, group, file_path, fields, **kwargs):
        #get parsed membership dicts
        
        subs = parse_subs_from_csv(file_path)
        
        for sub in subs:
            # create db entries here
        
        return subs
