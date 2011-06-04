from django.core.urlresolvers import reverse
from django.db import models

class Place(models.Model):
    name = models.CharField(blank=True, max_length=150)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    
    # meta
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode__(self):
        return self.display_name
    
    def get_absolute_url(self):
        return reverse('place_detail', args=[self.pk])
    
    @property
    def first_bit(self):
        try:
            return self.name.split(',')[0]
        except:
            return self.name
    
    @property
    def display_name(self):
        try:
            return "%s, %s" % (self.name.split(',')[0], self.name.split(',')[1])
        except:
            return self.name
    
    class Meta:
        unique_together = [('latitude', 'longitude')]
