from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class WeatherAPI(models.Model):
    apiname=models.CharField(max_length=120, null=False,unique=True)
    urllink=models.CharField(max_length=120, null=False,unique=True)
    querystring =models.TextField(blank=False, null=False)
    headers =models.TextField(blank=False, null=False)

    def __str__(self):
        return self.apiname
        
class Location(models.Model):
    description=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    lastupdate_at= models.DateTimeField(auto_now=True)
    parameters_link = models.CharField(max_length=120, blank=True, null=True)
    aggregation = models.TextField(blank=True, null=True)
    location_id = models.CharField(max_length=120, null=False,unique=False)
    location_name = models.CharField(max_length=120, null=False,unique=False)
    location_avail_params = models.TextField(blank=True, null=True)
    location_lat = models.CharField(max_length=120, null=False, default='0')
    location_lon = models.CharField(max_length=120, null=False, default='0')
    location_country = models.CharField(max_length=120, null=False, default='0')
    location_timezone = models.CharField(max_length=120, null=False, default='0')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='1')


    def __str__(self):
        return self.location_name 

    #def save(self, *args, **kwargs ):
    #    self.parameters_link = settings.SITE_URL + 'locations/' + str(self.id) + '/parameters/'
    #    super(Location, self).save(*args, **kwargs)


@receiver(post_save, sender=Location)      
def loc_para(sender, instance, created, **kwargs):
    if created:
        instance.parameters_link = settings.SITE_URL + 'locations/' + str(instance.id) + '/parameters/'
        instance.save()
    else:
        link=settings.SITE_URL + 'locations/' + str(instance.id) + '/parameters/'
        Location.objects.filter(pk=instance.id).update(parameters_link = link)




class Parameter(models.Model):
    name=models.CharField(max_length=120, null=False,unique=False)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)
    location_link = models.CharField(max_length=120, blank=False, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    lastupdate_at= models.DateTimeField(auto_now=True)
    latest_value = models.TextField(blank=True, null=True)
    values = models.TextField(blank=True, null=True)
    aggregation = models.TextField(blank=True, null=True)
    unitsofmeasurment = models.CharField(max_length=120, blank=False, null=False, default="metric")
    parameter_key_name=models.CharField(max_length=120, blank=False, null=False)

    def __str__(self):
        return self.name 

    #def save(self, *args, **kwargs ):
    #    self.location_link = settings.SITE_URL + 'locations/' + self.location
    #    super(Parameter, self).save(*args, **kwargs)

@receiver(post_save, sender=Parameter)
def para_loc(sender, instance, created, **kwargs):
    if created:
        instance.location_link = settings.SITE_URL + 'locations/' + str(instance.location_id)
        instance.save()
    else:
        link = settings.SITE_URL + 'locations/' + str(instance.location_id)
        Parameter.objects.filter(pk=instance.id).update(location_link = link)

