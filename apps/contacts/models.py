import uuid
from django.db import models
from django.contrib.auth.models import User
from perms.models import TendenciBaseModel
from timezones.fields import TimeZoneField
from contacts.managers import ContactManager

class Address(models.Model):
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

class Phone(models.Model):
    number = models.CharField(max_length=50, blank=True)

class Email(models.Model):
    email = models.EmailField()

class URL(models.Model):
    url = models.URLField()

class Company(models.Model):
    name = models.CharField(max_length=200, blank=True)
    addresses = models.ManyToManyField(Address, blank=True)
    phones = models.ManyToManyField(Phone, blank=True)
    emails = models.ManyToManyField(Email, blank=True)
    urls = models.ManyToManyField(URL, blank=True)

class Comment(models.Model):
    """
    Comments made after the contact has been created.
    Contacts will fill out a form and leave a message.
    These comments are added later to help describe the contact.
    """
    contact = models.ForeignKey('Contact', related_name='comments')
    comment = models.TextField()
    creator = models.ForeignKey(User)
    update_dt = models.DateTimeField(auto_now=True)
    create_dt = models.DateTimeField(auto_now_add=True)

class Contact(TendenciBaseModel):
    """
    Contact records are created when someone fills out a form.
    The form creates the contact with a message.
    Later the contact can be updated to include comments for
    further communication.
    """
    guid = models.CharField(max_length=40, default=uuid.uuid1)
    timezone = TimeZoneField()

    first_name = models.CharField(max_length=100, blank=True)
    middle_name= models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    suffix = models.CharField(max_length=5, blank=True)

    addresses = models.ManyToManyField(Address, blank=True)
    phones = models.ManyToManyField(Phone, blank=True)
    emails = models.ManyToManyField(Email, blank=True)
    urls = models.ManyToManyField(URL, blank=True)
    companies = models.ManyToManyField(Company, blank=True)

    message = models.TextField()

    # TODO: consider attachments

    objects = ContactManager()

    class Meta:
        permissions = (("view_contact","Can view contact"),)

    @models.permalink
    def get_absolute_url(self):
        return ("contact", [self.pk])

    def __unicode__(self):
        return "%s %s " % (self.first_name, self.last_name)