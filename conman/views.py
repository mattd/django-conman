from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from conman.models import Page

def base(request, uri):
    page = Page.objects.get_page_by_uri_or_404(uri)
    return render_to_response(
        'default.html',
        {'page': page,},
        context_instance = RequestContext(request)
    )
