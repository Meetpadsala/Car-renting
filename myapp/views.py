from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from uuid import uuid4
from urllib.parse import quote
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

# Stubbed views to unblock server - implement real logic next

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = login_table.objects.get(email_id=email, password=password)
            request.session['log_id'] = user.id
            request.session['log_user'] = user.name
            messages.success(request, f'Login successful, {user.name}!')
            return redirect('index')
        except login_table.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def searchcar(request):
    # TODO: search logic
    vehicles = Vehicle.objects.all()
    return render(request, 'searchcar.html', {'vehicles': vehicles})


def submitcontact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Contactus.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Contact message saved to database!')
    return redirect('contact')

def signup(request):
    statedetail = State.objects.all()
    citydetail = City.objects.all()
    areadetail = Area.objects.all()
    return render(request, 'signup.html', {'statedetail': statedetail, 'citydetail': citydetail, 'areadetail': areadetail})

def viewdata(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        usertype = request.POST['usertype']
        address = request.POST['address']
        pp = request.FILES.get('pp', None)
        
        # Check if user already exists
        if login_table.objects.filter(email_id=email).exists() or login_table.objects.filter(phone_no=phone).exists():
            messages.error(request, 'User with this email or phone already signed up. Please login.')
            return redirect('login')
        
        # Create user
        user = login_table(
            name=name,
            phone_no=phone,
            email_id=email,
            password=password,  # In production, hash password
            dob=dob,
            usertype=usertype,
            address=address,
            photo=pp
        )
        user.save()
        
        # Auto-login
        request.session['log_id'] = user.id
        request.session['log_user'] = user.name
        messages.success(request, f'Signup successful, welcome {user.name}! Please login.')
        return redirect('login')
    return redirect('signup')

def checklogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = login_table.objects.get(email_id=email, password=password)
            request.session['log_id'] = user.id
            request.session['log_user'] = user.name
            messages.success(request, f'Welcome back, {user.name}!')
            return JsonResponse({'status': 'success', 'redirect': '/index/'})
        except login_table.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def logout(request):
    request.session.flush()
    return redirect('index')

def profile(request):
    uid = request.session.get('log_id')
    if uid:
        user = login_table.objects.get(id=uid)
        return render(request, 'profile.html', {'userdata': user})
    return redirect('login')

def postacar(request):
    statedetail = State.objects.all()
    citydetail = City.objects.all()
    areadetail = Area.objects.all()
    return render(request, 'postacar.html', {'statedetail': statedetail, 'citydetail': citydetail, 'areadetail': areadetail})

def addacar(request):
    uid = request.session.get('log_id')
    if not uid:
        return redirect('login')
    statedetail = State.objects.all()
    citydetail = City.objects.all()
    areadetail = Area.objects.all()
    if request.method == 'POST':
        company = request.POST['cname']
        model_name = request.POST['model']
        model_year = request.POST['modelyear']
        base_rent_perday = request.POST['rent']
        location = request.POST['address']
        area_id = request.POST['area']
        city_id = request.POST['city']
        state_id = request.POST['state']
        model_photo = request.FILES['vp']
        rc_book = request.FILES['rc']
        vehicle = Vehicle(
            vendor_id=uid,
            company=company,
            model_name=model_name,
            model_year=model_year,
            base_rent_perday=base_rent_perday,
            location=location,
            area_id=area_id,
            city_id=city_id,
            state_id=state_id,
            model_photo=model_photo,
            rc_book=rc_book
        )
        vehicle.save()
        messages.success(request, 'Vehicle added successfully!')
        return redirect('mycars')
    return render(request, 'postacar.html', {'statedetail': statedetail, 'citydetail': citydetail, 'areadetail': areadetail})

def mycars(request):
    uid = request.session.get('log_id')
    if uid:
        cars = Vehicle.objects.filter(vendor_id=uid)
        return render(request, 'mycars.html', {'cars': cars})
    return redirect('login')

def allcars(request):
    cars = Vehicle.objects.annotate(avg_rating=Avg('feedback__rating')).all()
    return render(request, 'allcars.html', {'allcardata': cars})

def updatecardetails(request):
    # TODO: update car
    messages.success(request, 'Car updated')
    return redirect('mycars')

def bookcar(request):
    uid = request.session.get('log_id')
    if not uid:
        return redirect('login')
    if request.method == 'POST':
        car_id = request.POST.get('carid')
        booking_from = request.POST.get('bookingfrom')
        booking_to = request.POST.get('bookingto')
        payment = request.POST.get('payment')
        total_amount = request.POST.get('totalAmount', 0)
        vehicle = Vehicle.objects.get(id=car_id)
        booking = Booking.objects.create(
            user_id=uid,
            vehicle=vehicle,
            booking_from=booking_from,
            booking_to=booking_to,
            booking_amount=total_amount,
            payment_mode=payment,
            payment_status='Pending' if payment == 'offline' else 'Paid'
        )
        messages.success(request, 'Vehicle booked successfully! View all your bookings.')
        return redirect('userbookings')
    return render(request, 'booking.html')

def ownerbookings(request):
    uid = request.session.get('log_id')
    cars = Vehicle.objects.filter(vendor_id=uid)
    bookings = Booking.objects.filter(vehicle__in=cars)
    return render(request, 'ownerbookings.html', {'bookings': bookings})

def userbookings(request):
    uid = request.session.get('log_id')
    if uid:
        bookings = Booking.objects.filter(user_id=uid)
    else:
        bookings = Booking.objects.none()
    return render(request, 'userbookings.html', {'bookingdata': bookings})

def mycomplaints(request):
    uid = request.session.get('log_id')
    if uid:
        user = login_table.objects.get(id=uid)
        complaints = Complaint.objects.filter(user=user)
    else:
        complaints = []
        messages.error(request, 'Login required')
        return redirect('login')
    return render(request, 'mycomplaints.html', {'complaints': complaints})

def ownercomplaints(request):
    uid = request.session.get('log_id')
    if uid:
        user = login_table.objects.get(id=uid)
        cars = Vehicle.objects.filter(vendor=user)
        complaints = Complaint.objects.filter(vehicle__in=cars)
    else:
        complaints = []
        messages.error(request, 'Login required')
        return redirect('login')
    return render(request, 'ownercomplaints.html', {'complaints': complaints})

def givefeedback(request):
    uid = request.session.get('log_id')
    if uid:
        user = login_table.objects.get(id=uid)
        bookings = Booking.objects.filter(user=user, cancellation_status="No", booking_to__lt=timezone.now())
    else:
        bookings = []
    return render(request, 'givefeedback.html', {'bookings': bookings})

def submitfeedback(request):
    if request.method == 'POST':
        uid = request.session.get('log_id')
        booking_id = request.POST['booking_id']
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        booking = Booking.objects.get(id=booking_id)
        feedback = Feedback(
            user=login_table.objects.get(id=uid),
            vehicle=booking.vehicle,
            rating=rating,
            comment=comment
        )
        feedback.save()
        messages.success(request, f'Feedback submitted! {rating}/5 stars')
    return redirect('userbookings')

def complain(request):
    uid = request.session.get('log_id')
    vehicles = Vehicle.objects.all() if uid else []
    return render(request, 'complain.html', {'vehicles': vehicles})

def submitcomplain(request):
    if request.method == 'POST':
        uid = request.session.get('log_id')
        user = login_table.objects.get(id=uid)
        vehicle = Vehicle.objects.get(id=request.POST['vehicle'])
        description = request.POST['description']
        complaint = Complaint(user=user, vehicle=vehicle, description=description)
        complaint.save()
        messages.success(request, 'Complaint submitted successfully!')
    return redirect('profile')

def viewcar(request, cid):
    car = Vehicle.objects.get(id=cid)
    uid = request.session.get('log_id')
    Owner = False
    Mycar = False
    profiledata = None
    areadetail = Area.objects.all()
    citydetail = City.objects.all()
    statedetail = State.objects.all()
    if uid:
        userdata = login_table.objects.get(id=uid)
        Owner = userdata.usertype == 'Lessor'
        Mycar = car.vendor_id == uid
        profiledata = userdata
    context = {
        'cardata': car,
        'Owner': Owner,
        'Mycar': Mycar,
        'profiledata': profiledata,
        'areadetail': areadetail,
        'citydetail': citydetail,
        'statedetail': statedetail
    }
    return render(request, 'viewcar.html', context)

def removecar(request, rcid):
    # TODO: delete car
    messages.success(request, 'Car removed')
    return redirect('mycars')

def cancelbooking(request, booking_id):
    # TODO: cancel logic
    messages.success(request, 'Booking cancelled')
    return redirect('userbookings')

def edituserprofile(request):
    return render(request, 'edituserprofilepage.html')

def updateprofile(request):
    # TODO: update user
    messages.success(request, 'Profile updated')
    return redirect('profile')

def forgotpasswordpage(request):
    return render(request, 'forgotpasswordpage.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = login_table.objects.get(email_id=email)
            token = uuid4()
            expiry = timezone.now() + timedelta(hours=1)
            user.reset_token = token
            user.reset_expiry = expiry
            user.save()
            reset_link = f"http://127.0.0.1:8000/myapp/changepwdpage/?token={token}&email={quote(email)}"
            email_msg = EmailMessage(
                'Password Reset - Car Rental',
                f"Hi {user.name},\\n\\nClick to reset your password: {reset_link}\\n\\nThis link is valid for 1 hour.\\n\\nBest,\\nCar Rental Team",
                'rahulinfolabz@gmail.com',
                [email],
            )
            email_msg.send(fail_silently=True)
            messages.success(request, 'Reset link sent to your email. Check inbox/spam.')
        except login_table.DoesNotExist:
            messages.error(request, 'Email not found.')
        except Exception as e:
            print(f'Email error: {e}')
            messages.warning(request, 'Link generated but email delivery failed. Use direct link with token/email.')
    return redirect('login')

def changepwdpage(request):
    token = request.GET.get('token')
    email = request.GET.get('email')
    context = {}
    if token and email:
        try:
            user = login_table.objects.get(email_id=email, reset_token=token, reset_expiry__gt=timezone.now())
            context = {'token': token, 'email': email}
        except:
            messages.error(request, 'Invalid or expired reset link.')
            return redirect('login')
    return render(request, 'changepwdpage.html', context)

def changepwd(request):
    if request.method == 'POST':
        token = request.POST['token']
        email = request.POST['email']
        new_pwd = request.POST['new_pwd']
        confirm_pwd = request.POST['confirm_pwd']
        if new_pwd != confirm_pwd:
            messages.error(request, 'Passwords do not match.')
            return redirect('changepwdpage')
        try:
            user = login_table.objects.get(email_id=email, reset_token=token, reset_expiry__gt=timezone.now())
            user.password = new_pwd
            user.reset_token = None
            user.reset_expiry = None
            user.save()
            messages.success(request, 'Password reset successful. Please login.')
        except:
            messages.error(request, 'Invalid or expired token.')
        return redirect('login')

def ownercancel(request, booking_id):
    # TODO: owner cancel
    messages.success(request, 'Booking cancelled by owner')
    return redirect('ownerbookings')

def check_availability(request, vehicle_id):
    # AJAX stub
    return JsonResponse({'available': True})

def calculate_price(request, vehicle_id):
    # AJAX stub
    return JsonResponse({'price': 500})

