from locations.models import Location
from perms.utils import is_admin
from perms.forms import TendenciBaseForm
from django import forms

class LocationForm(TendenciBaseForm):

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'), ('pending','Pending'),))

    class Meta:
        model = Location
        fields = (
        'location_name',
        'description',
        'contact',
        'address',
        'address2',
        'city',
        'state',
        'zipcode',
        'country',
        'phone',
        'fax',
        'email',
        'website',
        'latitude',
        'longitude',
        'hq',
        'entity',
        'status',
        'status_detail',
        )

        fieldsets = [('Location Information', {
                      'fields': ['location_name',
                                 'description',
                                 'entity',
                                 'latitude',
                                 'longitude',
                                 'hq',
                                 ],
                      'legend': ''
                      }),
                      ('Contact', {
                      'fields': ['contact',
                                 'address',
                                 'address2',
                                 'city',
                                 'state',
                                 'zip_code',
                                 'country',
                                 'phone',
                                 'fax',
                                 'email',
                                 'website'
                                 ],
                        'classes': ['contact'],
                      }),
                      ('Permissions', {
                      'fields': ['allow_anonymous_view',
                                 'user_perms',
                                 'group_perms',
                                 ],
                      'classes': ['permissions'],
                      }),
                     ('Administrator Only', {
                      'fields': ['status',
                                 'status_detail'], 
                      'classes': ['admin-only'],
                    })]   
           
    def __init__(self, user=None, *args, **kwargs): 
        self.user = user
        super(LocationForm, self).__init__(user, *args, **kwargs)

        if not is_admin(user):
            if 'status' in self.fields: self.fields.pop('status')
            if 'status_detail' in self.fields: self.fields.pop('status_detail')
        
        
        