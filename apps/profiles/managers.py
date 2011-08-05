import operator

from django.db.models import Manager
from django.db.models import Q
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet

class ProfileManager(Manager):
    def create_profile(self, user):
        return self.create(user=user, 
                           creator_id=user.id, 
                           creator_username=user.username,
                           owner_id=user.id, 
                           owner_username=user.username, 
                           email=user.email)
        
    def search(self, query=None, *args, **kwargs):
        """
        Uses haystack to user.
        Returns a SearchQuerySet.
        Filter out users if they have hide_in_search set to True.
        """
        sqs = super(ProfileManager, self).search(query=query, *args, **kwargs)
        sqs = sqs.filter(hide_in_search=False)
        return sqs
