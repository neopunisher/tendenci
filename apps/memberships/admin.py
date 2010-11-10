from django.contrib import admin
from django.conf import settings
from django.template.defaultfilters import slugify
from memberships.models import MembershipType 
from memberships.models import MembershipApplication, MembershipApplicationPage, MembershipApplicationSection, MembershipApplicationField
from memberships.forms import MembershipTypeForm, MembershipApplicationForm
from user_groups.models import Group

class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'admin_fee', 'group', 'require_approval',
                     'renewal', 'expiration_method', 'corporate_membership_only',
                     'admin_only', 'status_detail']
    list_filter = ['name', 'price']
    
    fieldsets = (
        (None, {'fields': ('name', 'price', 'admin_fee', 'description')}),
        ('Expiration Method', {'fields': (
            ('type_exp_method'),)}),
        ('Other Options', {'fields': (
            'corporate_membership_only','corporate_membership_type_id',
            'require_approval','renewal','renewal_period_start', 
            'renewal_period_end', 'expiration_grace_period', 
            'admin_only', 'order',
            'status', 'status_detail')}),
    )
    
    form = MembershipTypeForm
    
    class Media:
        js = ("%sjs/jquery-1.4.2.min.js" % settings.STATIC_URL, 
              "%sjs/membtype.js" % settings.STATIC_URL,)
        
    
    def save_model(self, request, object, form, change):
        instance = form.save(commit=False)
        
        # save the expiration method fields
        type_exp_method = form.cleaned_data['type_exp_method']
        type_exp_method_list = type_exp_method.split(",")
        for i, field in enumerate(form.type_exp_method_fields):
            if field=='fixed_expiration_rollover':
                if type_exp_method_list[i]=='':
                    type_exp_method_list[i] = ''
            else:
                if type_exp_method_list[i]=='':
                    type_exp_method_list[i] = "0"

            exec('instance.%s="%s"' % (field, type_exp_method_list[i]))
         
        if not change:
            instance.creator = request.user
            instance.creator_username = request.user.username
            instance.owner = request.user
            instance.owner_username = request.user.username
            
            # create a group for this type
            group = Group()
            group.name = instance.name
            group.slug = slugify('membership %s' % group.name)
            # just in case, check if this slug already exists in group. 
            # if it does, make a unique slug
            tmp_groups = Group.objects.filter(slug__istartswith=group.slug)
            if tmp_groups:
                t_list = [g.slug[len(group.slug):] for g in tmp_groups]
                num = 1
                while str(num) in t_list:
                    num += 1
                group.slug = '%s%s' % (group.slug, str(num))
            
            group.label = instance.name
            group.email_recipient = request.user.email
            group.show_as_option = 0
            group.allow_self_add = 0
            group.allow_self_remove = 0
            group.description = "Auto-generated with the membership type. Used for membership only"
            group.notes = "Auto-generated with the membership type. Used for membership only"
            group.use_for_membership = 1
            
            group.creator = request.user
            group.creator_username = request.user.username
            group.owner = request.user
            group.owner_username = request.user.username
            
            group.save()
            
            instance.group = group
 
        # save the object
        instance.save()
        
        #form.save_m2m()
        
        return instance

class MembershipApplicationAdmin(admin.ModelAdmin):

    fieldsets = (
        (None,
            {
                'fields': (
                    'name','slug', 'notes', 'use_captcha', 'require_login',
                )
            },
        ),
    )

    prepopulated_fields = {'slug': ('name',)}
    form = MembershipApplicationForm

class MembershipApplicationPageAdmin(admin.ModelAdmin):
    list_display = ('ma', 'sort_order',)

class MembershipApplicationSectionAdmin(admin.ModelAdmin):
    list_display = ('ma', 'ma_page', 'label', 'description', 'admin_only', 'order', 'css_class')

class MembershipApplicationFieldAdmin(admin.ModelAdmin):
    list_display = ('ma', 'ma_section', 'object_type', 'label', 'field_name', 'field_type', 'size',
        'choices', 'required', 'visible', 'admin_only', 'editor_only', 'order', 'css_class',
    )

admin.site.register(MembershipType, MembershipTypeAdmin)
admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(MembershipApplicationPage, MembershipApplicationPageAdmin)
admin.site.register(MembershipApplicationSection, MembershipApplicationSectionAdmin)
admin.site.register(MembershipApplicationField, MembershipApplicationFieldAdmin)
