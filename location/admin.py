from django.contrib import admin

from .models import WeatherAPI, Location, Parameter

# Register your models here.


#model_list = [Location, Parameter]
#admin.site.register(model_list)

@admin.register(WeatherAPI, Location, Parameter)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]