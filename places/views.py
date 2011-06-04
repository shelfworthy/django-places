from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dg.views import template

from .models import Place

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    
    return template(request, 'places/detail.html', {
        'place': place.display_name,
        'content': True,
        'endpoint': True,
        'content_scroll': False,
        
        'point': place
    })