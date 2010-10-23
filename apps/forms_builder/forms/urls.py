from django.conf.urls.defaults import *


urlpatterns = patterns("forms_builder.forms.views",
    url(r"^$", "search", name="forms"),
    url(r"entries/export/(?P<id>\d+)$", "entries_export", name="form_entries_export"),
    url(r"entries/delete/(?P<id>\d+)$", "entry_delete", name="form_entry_delete"),
    url(r"add/$", "add", name="form_add"),
    url(r"update_fields/(?P<id>\d+)$", "update_fields", name="form_field_update"),
    url(r"edit/(?P<id>\d+)$", "edit", name="form_edit"),
    url(r"delete/(?P<id>\d+)$", "delete", name="form_delete"),
    url(r"entry/(?P<id>\d+)$", "entry_detail", name="form_entry_detail"),
    url(r"entries/(?P<id>\d+)$", "entries", name="form_entries"),
    url(r"(?P<slug>.*)/sent/$", "form_sent", name="form_sent"),
    url(r"(?P<slug>.*)/$", "form_detail", name="form_detail"),
)

