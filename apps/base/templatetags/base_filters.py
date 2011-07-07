import re
import os
import Image

from django.template import Library
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, strip_tags, urlize
from django.contrib.auth.models import AnonymousUser

register = Library()


@register.filter(name="localize_date")
def localize_date(value, to_tz=None):
    from timezones.utils import adjust_datetime_to_timezone
    try:
        if to_tz is None:
            to_tz=settings.UI_TIME_ZONE
            
        from_tz=settings.TIME_ZONE
        
        return adjust_datetime_to_timezone(value,from_tz=from_tz,to_tz=to_tz)
    except AttributeError:
        return ''

localize_date.is_safe = True


@register.filter_function
def date_short(value, arg=None):
    """Formats a date according to the given format."""
    from django.utils.dateformat import format
    from site_settings.utils import get_setting
    if not value:
        return u''
    if arg is None:
        s_date_format = get_setting('site','global','dateformat')
        if s_date_format:
            arg = s_date_format
        else:
            arg = settings.SHORT_DATETIME_FORMAT
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''
date_short.is_safe = False


@register.filter_function
def date_long(value, arg=None):
    """Formats a date according to the given format."""
    from django.utils.dateformat import format
    from site_settings.utils import get_setting
    if not value:
        return u''
    if arg is None:
        s_date_format = get_setting('site','global','dateformatlong')
        if s_date_format:
            arg = s_date_format
        else:
            arg = settings.DATETIME_FORMAT
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''
date_long.is_safe = False


@register.filter_function
def date(value, arg=None):
    """Formats a date according to the given format."""
    from django.utils.dateformat import format
    if not value:
        return u''
    if arg is None:
        arg = settings.DATETIME_FORMAT
    else:
        if arg == 'long':
            return date_long(value)
        if arg == 'short':
            return date_short(value)
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''
date_long.is_safe = False


@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.filter_function
def in_group(user, group):
    if group:
        if isinstance(user, AnonymousUser):
            return False
        return group in [dict['pk'] for dict in user.group_set.values('pk')]
    else:
        return False


@register.filter
def domain(link):
    from urlparse import urlparse
    link = urlparse(link)
    return link.hostname


@register.filter
def strip_template_tags(string):
    import re
    p = re.compile('{[#{%][^#}%]+[%}#]}')
    return re.sub(p,'',string)


@register.filter
@stringfilter      
def stripentities(value):
    """Strips all [X]HTML tags."""
    from django.utils.html import strip_entities
    return strip_entities(value)
stripentities.is_safe = True


@register.filter     
def format_currency(value):
    """format currency"""
    from base.utils import tcurrency
    return tcurrency(value)
format_currency.is_safe = True


@register.filter
def scope(object):
    return dir(object)


@register.filter
@stringfilter
def basename(path):
    from os.path import basename
    return basename(path)


@register.filter     
def date_diff(value, date_to_compare=None):
    """Compare two dates and return the difference in days"""
    import datetime
    if not isinstance(value, datetime.datetime):
        return 0
    
    if not isinstance(date_to_compare, datetime.datetime):
        date_to_compare = datetime.datetime.now()
    
    return (date_to_compare-value).days


@register.filter
def first_chars(string, arg):
    """ returns the first x characters from a string """
    string = str(string)
    if arg:
        if not arg.isdigit(): return string
        return string[:int(arg)]
    else:
        return string
    return string


@register.filter
def rss_date(value, arg=None):
    """Formats a date according to the given format."""
    from django.utils import formats
    from django.utils.dateformat import format
    from datetime import datetime

    if not value:
        return u''
    else:
        value = datetime(*value[:-3])
    if arg is None:
        arg = settings.DATE_FORMAT
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''
rss_date.is_safe = False


@register.filter()
def obfuscate_email(email, linktext=None, autoescape=None):
    """
    Given a string representing an email address,
    returns a mailto link with rot13 JavaScript obfuscation.
    
    Accepts an optional argument to use as the link text;
    otherwise uses the email address itself.
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    email = re.sub('@','\\\\100', re.sub('\.', '\\\\056', \
        esc(email))).encode('rot13')

    if linktext:
        linktext = esc(linktext).encode('rot13')
    else:
        linktext = email

    rotten_link = """<script type="text/javascript">document.write \
        ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (email, linktext)
    return mark_safe(rotten_link)
obfuscate_email.needs_autoescape = True


@register.filter_function
def split_str(s, args):
    """
    Split a string using the python string split method
    """
    if args:
        if isinstance(s, str):
            splitter = args[1]
            return s.split(splitter)
        return s
    return s


@register.filter
@stringfilter
def twitterize(value, autoescape=None):
    value = strip_tags(value)
    # Link URLs
    value = urlize(value, nofollow=False, autoescape=autoescape)
    # Link twitter usernames prefixed with @
    value = re.sub(r'(\s+|\A)@([a-zA-Z0-9\-_]*)\b',r'\1<a href="http://twitter.com/\2">@\2</a>&nbsp;',value)
    # Link hash tags
    value = re.sub(r'(\s+|\A)#([a-zA-Z0-9\-_]*)\b',r'\1<a href="http://search.twitter.com/search?q=%23\2">#\2</a>&nbsp;',value)
    return mark_safe(value)
twitterize.is_safe=True
twitterize.needs_autoescape = True

@register.filter
def thumbnail(file, size='200x200'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image.thumbnail([x, y], Image.ANTIALIAS)
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url

@register.filter_function
def datedelta(dt, range_):
    from datetime import datetime
    from datetime import timedelta
    from time import strftime

    range_type = 'add'
    # parse the range
    if '+' in range_:
        range_ = range_[1:len(range_)]
    if '-' in range_:
        range_type = 'subtract'
        range_ = range_[1:len(range_)]
    k, v = range_.split('=')
    set_range = {
        str(k): int(v)
    }

    # set the date
    if range_type == 'add':
        dt = dt + timedelta(**set_range)
    if range_type == 'subtract':
        dt = dt - timedelta(**set_range)

    return dt


@register.filter
def split(str,splitter):
    return str.split(splitter)
