from boxes.models import Box
from perms.utils import is_admin
from perms.forms import TendenciBaseForm
from django import forms
from tinymce.widgets import TinyMCE

class BoxForm(TendenciBaseForm):
    content = forms.CharField(required=False,
        widget=TinyMCE(attrs={'style':'width:100%'}, 
        mce_attrs={'storme_app_label':Box._meta.app_label, 
        'storme_model':Box._meta.module_name.lower()}))

    status_detail = forms.ChoiceField(
        choices=(('active','Active'),('inactive','Inactive'),))

    class Meta:
        model = Box
        
    def __init__(self, *args, **kwargs): 
        super(BoxForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = self.instance.pk
        else:
            self.fields['content'].widget.mce_attrs['app_instance_id'] = 0