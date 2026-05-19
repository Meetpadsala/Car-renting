from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Avg, Count
from .models import login_table, Vehicle, Area, City, State, Booking, Complaint, Feedback

def index(request):
    try:
        uid = request.session['log_id']
        userdata = login_table.objects.get(id=uid)
        Owner = False
        if userdata.usertype == "Lessor":
            Owner = True

        statedetail = State.objects.all()
        citydetail = City.objects.all()
        areadetail = Area.objects.all()
        allcardata = Vehicle.objects.annotate(avg_rating=Avg('feedback__rating'), num_reviews=Count('feedback')).all().order_by('-id')

        context = {
            'userdata': userdata,
            'Owner': Owner,
            'statedetail': statedetail,
            'citydetail': citydetail,
            'areadetail': areadetail,
            'allcardata': allcardata,
        }
        return render(request, 'index.html', context)
    except:
        pass
    statedetail = State.objects.all()
    citydetail = City.objects.all()
    areadetail = Area.objects.all()
    allcardata = Vehicle.objects.annotate(avg_rating=Avg('feedback__rating'), num_reviews=Count('feedback')).all().order_by('-id')
    context = {
        'statedetail': statedetail,
        'citydetail': citydetail,
        'areadetail': areadetail,
        'allcardata': allcardata,
    }
    return render(request,'index.html', context)

# [All other functions remain the same - copy from current views.py]
# Note: Replace the full file with this template + paste existing functions.
# This template has correct imports.

# To apply: cd CarRenting1 && cp views_fixed.py views.py

