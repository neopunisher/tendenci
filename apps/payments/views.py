from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from payments.models import Payment
from payments.authorizenet.utils import prepare_authorizenet_sim_form
from invoices.models import Invoice
from base.http import Http403

def pay_online(request, invoice_id, guid="", template_name="payments/pay_online.html"):
    # check if they have the right to view the invoice
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if not invoice.allow_view_by(request.user, invoice.guid): return Http403
    
    # tender the invoice
    if not invoice.is_tendered:
        invoice.tender()
      
    # generate the payment
    payment = Payment()
    
    boo = payment.payments_pop_by_invoice_user(request.user, invoice, invoice.guid)
    
    # post payment form to gateway and redirect to the vendor so customer can pay from there
    if boo:
        # merchant_account = getSetting("global", "MerchantAccount")
        merchant_account = "authorizenet"
        if merchant_account == "authorizenet":
            form = prepare_authorizenet_sim_form(request, payment)
            post_url = settings.AUTHNET_TEST_POST_URL
        else:   # more vendors 
            form = None
            post_url = ""
    else:
        form = None
        post_url = ""
    return render_to_response(template_name, 
                              {'form':form, 'post_url':post_url}, 
                              context_instance=RequestContext(request))

        

