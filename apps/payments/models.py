from django.db import models
from django.contrib.auth.models import User
from invoices.models import Invoice

RESPONSE_CODE_CHOICES = (
    ('1', 'This transaction has been approved'),
    ('2', 'This transaction has been declined'),
    ('3', 'There has been an error processing this transaction'),
    ('4', 'This transaction is being held for review'),
)

AVS_RESPONSE_CODE_CHOICES = (
    ('A', 'Address (Street) matches, ZIP does not'),
    ('B', 'Address information not provided for AVS check'),
    ('E', 'AVS error'),
    ('G', 'Non-U.S. Card Issuing Bank'),
    ('N', 'No Match on Address (Street) or ZIP'),
    ('P', 'AVS not applicable for this transaction'),
    ('R', 'Retry - System unavailable or timed out'),
    ('S', 'Service not supported by issuer'),
    ('U', 'Address information is unavailable'),
    ('W', 'Nine digit ZIP matches, Address (Street) does not'),
    ('X', 'Address (Street) and nine digit ZIP match'),
    ('Y', 'Address (Street) and five digit ZIP match'),
    ('Z', 'Five digit ZIP matches, Address (Street) does not'),
)

METHOD_CHOICES = (
    ('CC', 'Credit Card'),
    ('ECHECK', 'eCheck'),
)

TYPE_CHOICES = (
    ('auth_capture', 'Authorize and Capture'),
    ('auth_only', 'Authorize only'),
    ('credit', 'Credit'),
    ('prior_auth_capture', 'Prior capture'),
    ('void', 'Void'),
)


class PaymentManager(models.Manager):
    def create_from_dict(self, params):
        kwargs=dict(map(lambda x: (str(x[0][2:]), x[1]), params.items()))
        return self.create(**kwargs)

    def create_from_list(self, items):
        kwargs=dict(zip(map(lambda x: x.name, Payment._meta.fields)[1:], items))
        return self.create(**kwargs)


class Payment(models.Model):
    guid = models.CharField(max_length=50)
    invoice = models.ForeignKey(Invoice)
    payment_attempted = models.BooleanField(default=1)
    response_code = models.CharField(max_length=2, default='')
    response_subcode = models.CharField(max_length=10, default='')
    response_reason_code = models.CharField(max_length=15, default='')
    response_reason_text = models.TextField(default='')
    response_page = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=100, default='')
    trans_string = models.CharField(max_length=100)
    po_num = models.CharField(max_length=50, blank=True)
    auth_code = models.CharField(max_length=10)
    avs_code = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    invoice_num = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=1600)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=60)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=255)
    ship_to_first_name = models.CharField(max_length=100, blank=True)
    ship_to_last_name = models.CharField(max_length=100, blank=True)
    ship_to_company = models.CharField(max_length=50, blank=True)
    ship_to_address = models.CharField(max_length=60, blank=True)
    ship_to_city = models.CharField(max_length=40, blank=True)
    ship_to_state = models.CharField(max_length=40, blank=True)
    ship_to_zip = models.CharField(max_length=20, blank=True)
    ship_to_country = models.CharField(max_length=60, blank=True)
    method = models.CharField(max_length=10)
    freight = models.CharField(max_length=16, blank=True)
    tax_exempt = models.CharField(max_length=16, blank=True)
    md5_hash = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=20)
    cust_id = models.CharField(max_length=20, default=0)
    tax = models.CharField(max_length=16, blank=True)
    duty = models.CharField(max_length=16, blank=True)
    verified = models.BooleanField(blank=True, default=False)
    submit_dt = models.DateTimeField(blank=True, null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="payment_creator",  null=True)
    creator_username = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, related_name="payment_owner", null=True)
    owner_username = models.CharField(max_length=50, null=True)
    status_detail = models.CharField(max_length=50, default='estimate')
    status = models.BooleanField(default=True)

    objects = PaymentManager()

    @property
    def is_approved(self):
        return self.response_code=='1'

    def __unicode__(self):
        return u"response_code: %s, trans_id: %s, amount: %.2f" % (self.response_code, self.trans_id, self.amount)
    
    def payments_pop_by_invoice_user(self, user, inv, guid='', **kwargs):
        from django.core.urlresolvers import reverse
        boo = False
        if inv.allow_payment_by(user, guid):
            boo = True
            self.first_name = inv.bill_to_first_name
            self.last_name = inv.bill_to_last_name
            self.company = inv.bill_to_company
            self.phone = inv.bill_to_phone
            self.email = inv.bill_to_email
            if user and user.id:
                self.cust_id = user.id
            self.address = inv.bill_to_address
            self.city = inv.bill_to_city
            self.state = inv.bill_to_state  
            self.zip = inv.bill_to_zip_code
            self.country = inv.bill_to_country
            
            self.fax = inv.bill_to_fax
            self.ship_to_first_name = inv.ship_to_first_name
            self.ship_to_last_name = inv.ship_to_last_name
            self.ship_to_company = inv.ship_to_company
            self.ship_to_address = inv.ship_to_address
            self.ship_to_city = inv.ship_to_city
            self.ship_to_state = inv.ship_to_state
            self.ship_to_zip = inv.ship_to_zip_code
            self.ship_to_country = inv.ship_to_country
            self.amount = inv.balance
            self.invoice = inv
            # hard coded here - same as in T4
            self.method = 'cc'
            self.status = 1
            
            # description
            if inv.invoice_object_type == 'make_payment':
                self.description = 'Tendenci Invoice %d Payment (ID# %d).' % (inv.id, inv.invoice_object_type_id) 
            else:
                self.description = 'Tendenci Invoice %d Payment.' % (inv.id)
                
            # save the payment because we need the payment id below
            self.save()
            
            # site_url - need to use site setting here
            site_url = "http://tendenci5.schipul.net"
            #merchant_account = getSetting("global", "MerchantAccount")
            merchant_account = "authorizenet"
            if merchant_account == "authorizenet":
                self.response_page = site_url + reverse('authorizenet.sim_thank_you', args=[self.id])
            else:
                self.response_page = site_url + "/payments/thankyou/%d" % (self.id)
                
            self.invoice_num = self.id  
            self.save()
            
        return boo
            
                
            
            
            
            
            
    