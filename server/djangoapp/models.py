from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
        ('TRUCK', 'Truck'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField(
        default=2023,
        validators=[MaxValueValidator(2023), MinValueValidator(2015)],
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"


class Dealer(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    st = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.full_name} ({self.city}, {self.state})"


class Review(models.Model):
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(default=now)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.CharField(max_length=10, blank=True)
    sentiment = models.CharField(max_length=20, default='neutral')

    def __str__(self):
        return f"Review by {self.name} for {self.dealership.full_name}"