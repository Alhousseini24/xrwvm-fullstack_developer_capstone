from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review

admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Dealer)
admin.site.register(Review)
