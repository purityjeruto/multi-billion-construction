import json

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from django.contrib import messages

from multibillionapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from multibillionapp.models import appointment, Transaction


# Create your views here.
def about (request):
    return render(request,'about.html')
def blog_details (request):
    return render(request,'blog_details.html')
def starter(request):
    return render(request,'starter-page.html')
def blog(request):
    return render(request,'blog.html')
def contact(request):
    return render(request,'contact.html')
def index(request):
    return render(request,'index.html')
def project_details(request):
    return render(request,'project_details.html')
def projects(request):
    return render(request,'projects.html')
def services_details(request):
    return render(request,'services_details.html')
def services(request):
    return render(request,'services.html')
def appointment1(request):
    if request.method =='POST':
       myappointments = appointment(
            name = request.POST['name'],
            email = request.POST['email'],
            phone= request.POST['phone'],
            date = request.POST['date'],
            department= request.POST['department'],
           contractor = request.POST['contractor'],

        )
       myappointments.save()
       return redirect('/show')

    else:
          return render(request,'appointment.html')

def contact1(request):
    if request.method =='POST':
       mycontacts = contact(
            name = request.POST['name'],
            email = request.POST['email'],
            subject= request.POST['subject'],
            message = request.POST['message'],
        )
       mycontacts.save()
       return redirect('/contact')

    else:
          return render(request,'contact.html')

def show (request):
    all=appointment.objects.all()
    return render(request, 'show.html',{'all':all})

def delete(request,id):
    deleteappointment=appointment.objects.get(id=id)
    deleteappointment.delete()
    return redirect('/show')

def edit(request,id):
    appointment1= get_object_or_404(appointment,id=id)
    if request.method =='POST':
            appointment1.name = request.POST['name'],
            appointment1.email = request.POST['email'],
            appointment1.phone= request.POST['phone'],
            appointment1.date= request.POST['date'],
            appointment1.department= request.POST['department'],
            appointment1.doctor= request.POST['doctor'],
            appointment1.message = request.POST['message']
            appointment1.save()
            return redirect('/show')
    else:
        return render(request, 'edit.html', {'appointment1': appointment1})

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/index')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')

#Mpesa Api
def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        # Parse response
        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        # Save transaction to database
        transaction = Transaction(
            phone_number=phone,
            amount=amount,
            transaction_id=transaction_id,
            status="Success" if result_code == "0" else "Failed"
        )
        transaction.save()

        return HttpResponse(
            f"Transaction ID: {transaction_id}, Status: {'Success' if result_code == '0' else 'Failed'}")


def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
