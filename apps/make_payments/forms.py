from django import forms
from django.contrib.auth.models import User
from make_payments.models import MakePayment

class MakePaymentForm(forms.ModelForm):
    # get the payment_method choices from settings

    # TODO: Make check-paid an admin only option
    #payment_method = forms.CharField(widget=forms.RadioSelect(choices=(('check-paid', 'Paid by Check'),
    #                                                          ('cc', 'Make Online Payment'),)), initial='cc', )
    payment_method = forms.CharField(widget=forms.RadioSelect(choices=(('cc', 'Make Online Payment'),)), initial='cc',)
    company = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'size':'30'}))
    address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size':'35'}))
    state = forms.CharField(max_length=50, required=False,  widget=forms.TextInput(attrs={'size':'5'}))
    zip_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'size':'10'}))
    referral_source = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size':'40'}))
    email = forms.EmailField(help_text='A valid e-mail address, please.')
    email_receipt = forms.BooleanField(initial=True)
    
    class Meta:
        model = MakePayment
        fields = ('payment_amount',
                  'payment_method',
                  'first_name',
                  'last_name',
                  'company',
                  'address',
                  'address2',
                  'city',
                  'state',
                  'zip_code',
                  'country',
                  'phone',
                  'email',
                  'email_receipt',
                  'referral_source',
                  'comments',
                  )
        
    def __init__(self, user, *args, **kwargs):
        super(MakePaymentForm, self).__init__(*args, **kwargs)
        # populate the user fields
        if user and user.id:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            try:
                profile = user.get_profile()
                if profile:
                    self.fields['company'].initial = profile.company
                    self.fields['address'].initial = profile.address
                    self.fields['address2'].initial = profile.address2
                    self.fields['city'].initial = profile.city
                    self.fields['state'].initial = profile.state
                    self.fields['zip_code'].initial = profile.zipcode
                    self.fields['country'].initial = profile.country
                    self.fields['phone'].initial = profile.phone
            except:
                pass
        