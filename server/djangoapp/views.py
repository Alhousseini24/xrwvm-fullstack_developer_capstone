from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review
from .populate import initiate

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    username_exist = User.objects.filter(username=username).exists()
    email_exist = User.objects.filter(email=email).exists()
    if not username_exist and not email_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)

def get_dealerships(request, state=None):
    if state is None:
        dealerships = Dealer.objects.all()
    else:
        dealerships = Dealer.objects.filter(state__iexact=state)
    dealership_list = [{"id": d.id, "city": d.city, "state": d.state, "st": d.st, "address": d.address, "zip": d.zip, "lat": d.lat, "long": d.long, "short_name": d.short_name, "full_name": d.full_name} for d in dealerships]
    return JsonResponse({"status": 200, "dealers": dealership_list})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        reviews = Review.objects.filter(dealership_id=dealer_id)
        review_list = [{"id": r.id, "name": r.name, "dealership": r.dealership_id, "review": r.review, "purchase": r.purchase, "purchase_date": r.purchase_date, "car_make": r.car_make, "car_model": r.car_model, "car_year": r.car_year, "sentiment": r.sentiment} for r in reviews]
        return JsonResponse({"status": 200, "reviews": review_list})
    return JsonResponse({"status": 400, "message": "Bad Request"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        dealer = get_object_or_404(Dealer, pk=dealer_id)
        reviews = Review.objects.filter(dealership_id=dealer_id)
        review_list = [{"id": r.id, "name": r.name, "review": r.review, "purchase": r.purchase, "purchase_date": r.purchase_date, "car_make": r.car_make, "car_model": r.car_model, "car_year": r.car_year, "sentiment": r.sentiment} for r in reviews]
        dealer_data = {"id": dealer.id, "full_name": dealer.full_name, "city": dealer.city, "state": dealer.state, "address": dealer.address, "zip": dealer.zip}
        return JsonResponse({"status": 200, "dealer": dealer_data, "reviews": review_list})
    return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            review = Review(dealership_id=data["dealership"], name=data.get("name", ""), review=data["review"], purchase=data.get("purchase", False), purchase_date=data.get("purchase_date") or None, car_make=data.get("car_make", ""), car_model=data.get("car_model", ""), car_year=data.get("car_year", ""), sentiment="neutral")
            review.save()
            return JsonResponse({"status": 200, "message": "Review added successfully"})
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            return JsonResponse({"status": 500, "message": "Error adding review"})
    return JsonResponse({"status": 405, "message": "Method Not Allowed"})

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})