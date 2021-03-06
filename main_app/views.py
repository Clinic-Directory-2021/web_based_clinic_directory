from django.shortcuts import render, redirect
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from django.http import HttpResponse
from pyasn1.type.univ import Null

import pyrebase
import firebase_admin
import requests
import json

import folium

import datetime

from django.template.loader import render_to_string
from django.template import loader

import time
from django.core.mail import send_mail

from django.core.paginator import Paginator

import pytz

config={
    "apiKey": "AIzaSyDwWsW--ZHaZIOE4OXu5VhMIclZad8zDYw",
    "authDomain": "animal-clinic-directory-2021.firebaseapp.com",
    "databaseURL": "https://animal-clinic-directory-2021-default-rtdb.firebaseio.com/",
    "projectId": "animal-clinic-directory-2021",
    "storageBucket": "animal-clinic-directory-2021.appspot.com",
    "messagingSenderId": "165228810397",
    "appId": "1:165228810397:web:8378bcc8cb06dd52520474",
    "measurementId": "G-D4BEP96KMK"
}

firebase = pyrebase.initialize_app(config)
cred = credentials.Certificate("main_app/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

auth = firebase.auth()
db = firebase.database()
firestoreDB = firestore.client()

storage = firebase.storage()

# Create your views here.

def index(request):
    #map Size
    request.session['session'] = "dashboard"
    f = folium.Figure(width=880, height=700)

    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

    timeNow = datetime.datetime.now().time()
    date_time = timeNow.strftime('%I:%M %p')
    currentTime = datetime.datetime.strptime(date_time, '%I:%M %p').time()

    users = firestoreDB.collection('users').get()

    user_data = []

    for user in users:
        value = user.to_dict()

        opening_time = datetime.datetime.strptime(value['opening_time'], '%I:%M %p').time()

        closing_time = datetime.datetime.strptime(value['closing_time'], '%I:%M %p').time()

        # opening_time = value['opening_time'].strftime('%I:%M %p')

        # closing_time = value['closing_time'].strftime('%I:%M %p')

        if opening_time < currentTime and currentTime < closing_time:
            value['isOpen'] = "True"
            # user_data.append(value)
        
        user_data.append(value)

        latitude = value['latitude']
        longitude = value['longitude']
        # commented line removed 5 star image +"<br><br><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><br>5.0" 
        folium.Marker([latitude, longitude], 
        popup= "<img style=\"width:200px;\" src=\""+value['clinic_img_url']+"\">"
        +"<b>Clinic Name:</b><br>" + value['clinic_name'] + "<br><br><b>Clinic Address:</b><br>" 
        + value['clinic_address']  +
         "<br><br><b>Open and Closing time:</b><br>" + value['opening_time'] +
          " - " + value['closing_time'] + "<br><br><em>Description:</em><br>"+
           value['clinic_description']  +"<br><br><b>Contact number:</b><br>" +
            value['clinic_contact_number'] , 
        icon=folium.Icon(color="red", icon="fa-paw", prefix='fa'),
        tooltip= value['clinic_name']).add_to(map)
        

    paginator = Paginator(user_data, 3)
    page_number = request.GET.get('page') or 1
    item_list = paginator.get_page(page_number)
    
    # Get html representation of the map
    map = map._repr_html_()

    if request.method == 'POST':
        userId = request.POST.get('user_id_post')
        items = firestoreDB.collection('items').document(userId).get()

        data = {
            'map': map,
            'user_data': user_data,
            'item_data': items.to_dict(),
         }
        return render(request, 'item_data.html', {'item_data':items.to_dict()})
        #return HttpResponse(json.dumps(items.to_dict()))
    else:
        data = {
            'map': map,
            'user_data': user_data,
            "session":request.session['session'],
            'currentTime': currentTime, 
            'opening_time': opening_time,
            'closing_time': closing_time,
            'item_list':item_list,
            'category': 'all',
            'categoryLabel': 'All Establishments',
        }
    
    if 'user_id' not in request.session:
        return render(request,'index.html', data)
    else:
        return redirect('/homepage')


def getSearchData(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_item')

    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        user_data.append(value)

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

    return render(request, 'search_suggest.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
        })

def login(request):
    #meaning if user_id session variable is not set then execute this code
    request.session['session'] = "login"
    if 'user_id' not in request.session:
        return render(request,'login.html',{"session":request.session['session']})
    else:
        return redirect('/homepage')

def homepage(request):
    request.session['session'] = "homepage"
    if 'user_id' in request.session:
        user_data = firestoreDB.collection('users').document(request.session['user_id']).get()

        item_data = firestoreDB.collection('items').document(request.session['user_id']).get()

        appointment_queue = firestoreDB.collection('appointment_queue').where('user_id' , '==', request.session['user_id']).stream()

        appointment_total = 0

        for appointment in appointment_queue:
            appointment_total = appointment_total + 1

        return render(request,'homepage.html', {
        'appointment_total': str(appointment_total),
        'user_data': user_data.to_dict(),
        'item_data': item_data.to_dict(),
        'session':request.session['session']
        })
    else:
        return redirect('/login')

def register(request):
    #create Map and zoom on Malolos, Bulacan Philippines
    request.session['session'] = "register"
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13)

    map.add_child(folium.LatLngPopup())

    #map.add_child(folium.ClickForMarker())

    # Get html representation of the map
    map = map._repr_html_()

    

    #Store the html representation of the map to data variable
    data = {
        'map': map,
        "session":request.session['session']
    }

    return render(request,'register.html', data)

def register_user_firebase(request):
    clinicImage =  request.FILES['clinicImage']
    fileName = request.POST.get('fileName')
    

    clinicName = request.POST.get('clinicName')
    clinicAddress = request.POST.get('clinicAddress')
    clinicContact = request.POST.get('clinicContact')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    opening_time = request.POST.get('opening_time')
    closing_time = request.POST.get('closing_time')
    clinicDescription = request.POST.get('clinicDescription')
    clinicCategory = request.POST.get('clinicCategory')
    

    opening_timeCheck = datetime.datetime.strptime(opening_time, '%I:%M %p').time()

    closing_timeCheck = datetime.datetime.strptime(closing_time, '%I:%M %p').time()

    if opening_timeCheck > closing_timeCheck:
        return HttpResponse('Time Error')
    else:
        if password == confirm_password:
            try:
                #register email and password to firebase auth
                user = auth.create_user_with_email_and_password(email, password)

                img_file_directory = user['localId']+"/clinic_images/"+ fileName

                #upload product image
                storage.child(img_file_directory).put(clinicImage, user['localId'])
                
                # now = datetime.datetime.now()
                tz = pytz.timezone('Asia/Hong_Kong')
                now = datetime.datetime.now(tz)


                doc_ref = firestoreDB.collection('queue').document(user['localId'])
                doc_ref.set({
                    'user_id': user['localId'],
                    'clinic_img_url' : storage.child(img_file_directory).get_url(user['localId']),
                    'clinic_img_directory' : img_file_directory,
                    'clinic_name': clinicName,
                    'clinic_address': clinicAddress,
                    'clinic_contact_number': clinicContact,
                    'latitude': latitude,
                    'longitude': longitude,
                    'email': email,
                    'opening_time': opening_time,
                    'closing_time': closing_time,
                    'clinic_description': clinicDescription,
                    'total_items': 0,
                    'clinicCategory': clinicCategory,
                    'request_date': now,
                })
                #messages.success(request, "New User Registered Successfully!")
                return HttpResponse('New User Registered Successfully!')
            except requests.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                if error == "EMAIL_EXISTS":
                    #messages.success(request, "Email Already Exists!")
                    return HttpResponse('Email Already Exists!')

        else:
            #messages.success(request, "Password Do not Match!")
            return HttpResponse('Password Do not Match!')

def login_validation(request):
    email = request.POST.get('login_email')
    password = request.POST.get('login_password')
    
    users = firestoreDB.collection('users').get()

    try:
        user_signin = auth.sign_in_with_email_and_password(email,password)
        
        for user in users:
            value = user.to_dict()
            if value['email'] == email:
              request.session['user_id'] = user_signin['localId']
              request.session['clinic_name'] = value['clinic_name']
              return HttpResponse('Success!')

        return HttpResponse('Invalid Email or Password!')
    except:
        return HttpResponse('Invalid Email or Password!')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('/')
    return redirect('/')

def settings(request):
    request.session['session'] = "settings"

    if 'user_id' in request.session:
        #map Size
        f = folium.Figure(width=800, height=500)

        #create Map and zoom on Malolos, Bulacan Philippines
        map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

        map.add_child(folium.LatLngPopup())

        #map.add_child(folium.ClickForMarker())

        # Get html representation of the map
        map = map._repr_html_()

        result = firestoreDB.collection('users').document(request.session['user_id']).get()
        result.to_dict()

        dict_data = result.to_dict()

        open_time = dict_data['opening_time']

        close_time = dict_data['closing_time']

        open_time = datetime.datetime.strptime(open_time, '%I:%M %p')

        close_time = datetime.datetime.strptime(close_time, '%I:%M %p')

        print(open_time.strftime("%H:%M"))
        print(close_time.strftime("%H:%M"))

        appointment_queue = firestoreDB.collection('appointment_queue').where('user_id' , '==', request.session['user_id']).stream()

        appointment_total = 0

        for appointment in appointment_queue:
            appointment_total = appointment_total + 1

        return render(request,'settings.html', {
            'user_data': result.to_dict(),
            'map': map,
            'session':request.session['session'],
            'open_time': open_time.strftime("%H:%M"),
            'close_time': close_time.strftime("%H:%M"),
            'appointment_total': appointment_total,

            })
    else:
        return redirect('/login')

def save_clinic_info(request):
    clinicImage =  request.FILES['clinicImage']
    fileName = request.POST.get('fileName')
    img_file_directory = request.session['user_id']+"/clinic_images/"+ fileName
    old_img_file_directory = request.POST.get('old_image_directory')

    editClinicName = request.POST.get('editClinicName')
    editClinicAddress = request.POST.get('editClinicAddress')
    clinicContact = request.POST.get('clinicContact')
    editLatitude = request.POST.get('editLatitude')
    editLongitude = request.POST.get('editLongitude')
    opening_time = request.POST.get('opening_time')
    closing_time = request.POST.get('closing_time')
    editClinicDescription = request.POST.get('editClinicDescription')

    doc_ref = firestoreDB.collection('users').document(request.session['user_id'])

    #delete the old picture
    storage.delete(old_img_file_directory, request.session['user_id'])
    
    #upload product image
    storage.child(img_file_directory).put(clinicImage, request.session['user_id'])


    opening_timeCheck = datetime.datetime.strptime(opening_time, '%I:%M %p').time()

    closing_timeCheck = datetime.datetime.strptime(closing_time, '%I:%M %p').time()

    if opening_timeCheck > closing_timeCheck:
        return HttpResponse('Time Error')
    else:
        doc_ref.update({
            'clinic_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
            'clinic_img_directory' : img_file_directory,
            'clinic_address': editClinicAddress,
            'clinic_contact_number': clinicContact,
            'clinic_name': editClinicName,
            'latitude': editLatitude,
            'longitude': editLongitude,
            'clinic_description': editClinicDescription,
            'opening_time': opening_time,
            'closing_time': closing_time,
            })
        return HttpResponse('Information Updated Successfully!')

def add_item(request):
    if 'user_id' in request.session:
        user_data = firestoreDB.collection('users').document(request.session['user_id']).get()
        return render(request,'add_item.html', {
            'user_data': user_data.to_dict(),
        })
    else:
        return redirect('/login')

def add_item_firebase(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])

    try:
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        field_name = request.POST.get('field_name')
        product_image = request.FILES['selected_product_image']
        img_fileName = product_image.name
        img_file_directory = request.session['user_id']+"/product_images/"+ img_fileName

        productCategory = request.POST.get('productCategory')
        product_description = request.POST.get('product_description')
        
        #if fields are not null then try to update the document on items,
        #if that document is not yet existing then create one
        if product_name != "" and product_price != "" and field_name != "" and product_image != "" and img_fileName != "" and img_file_directory != "":
            
            #upload product image
            storage.child(img_file_directory).put(product_image, request.session['user_id'])
            
            try:
                items_doc_ref.update({
                field_name: {
                    'belong_to': request.session['user_id'],
                    'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                    'product_img_directory' : img_file_directory,
                    'product_name': product_name,
                    'product_price': product_price,
                    'availability': "available",
                    'product_category': productCategory,
                    'product_description': product_description,
                    }
                })
            except:
                items_doc_ref.set({
                field_name: {
                        'belong_to': request.session['user_id'],
                        'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                        'product_img_directory' : img_file_directory,
                        'product_name': product_name,
                        'product_price': product_price,
                        'availability': "available",
                        'product_category': productCategory,
                        'product_description': product_description,
                        }
                    })
            #increment the total number of items in a specific user
            users_doc_ref = firestoreDB.collection('users').document(request.session['user_id'])
            users_doc_ref.update({"total_items": firestore.Increment(1)})
            return redirect('/')
        else:
            messages.success(request, "Please Fill up all the forms")
            return render(request,'add_item.html')
    except:
        messages.success(request, "Please upload product image first")
        return render(request,'add_item.html')
   
def edit_item_firebase(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])

    try:
        product_name = request.POST.get('edit_prod_name')
        product_price = request.POST.get('edit_prod_price')
        field_name = request.POST.get('edit_field_name')
        product_image = request.FILES['selected_edit_product_image']
        img_fileName = product_image.name
        img_file_directory = request.session['user_id']+"/product_images/"+ img_fileName
        old_img_file_directory = request.POST.get('old_image_directory')

        edit_prod_description = request.POST.get('edit_prod_description')
        edit_prod_category = request.POST.get('edit_prod_category')
        
        #if fields are not null then try to update the document on items,
        #if that document is not yet existing then create one
        if product_name != "" and product_price != "" and field_name != "" and product_image != "" and img_fileName != "" and img_file_directory != "" and old_img_file_directory != "":
            
            #delete the old picture
            storage.delete(old_img_file_directory, request.session['user_id'])

            #upload product image
            storage.child(img_file_directory).put(product_image, request.session['user_id'])

            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'product_category': edit_prod_category,
                'product_description': edit_prod_description,
                'availability': "available",
                }
            })

            return redirect('/')
        else:
            messages.success(request, "Please Fill up all the forms")
            return render(request,'homepage.html')
    except:
        messages.success(request, "Please upload product image first")
        return render(request,'homepage.html')   
    
def product_item_availability(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])
    if request.method == 'POST':
        availability = request.POST.get('availability')
        field_name = request.POST.get('product_key')

        product_name = request.POST.get('prod_name')
        product_price = request.POST.get('prod_price')
        product_image_url = request.POST.get('prod_img_url')
        img_file_directory = request.POST.get('prod_img_directory')
        category = request.POST.get('categ')
        description = request.POST.get('desc')

        if availability == 'available':
            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : product_image_url,
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'product_category': category,
                'product_description': description,
                'availability': "available",
                }
            })
        if availability == 'not available':
            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'product_category': category,
                'product_description': description,
                'availability': "not available",
                }
            })

    return HttpResponse('')

def search_item(request):
    searchField = request.POST.get('searchField')

    if 'user_id' in request.session:
        user_data = firestoreDB.collection('users').document(request.session['user_id']).get()

        item_data = firestoreDB.collection('items').document(request.session['user_id']).get()

        return render(request,'homepage_search.html', {
        'user_data': user_data.to_dict(),
        'item_data': item_data.to_dict(),
        'searchField': searchField,
        })
    else:
        return redirect('/login')

def search_clinic(request):
    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    search_item = request.POST.get('search_item')
    category = request.POST.get('category')

    user_data = []

    item_data = []

    if category == 'all':
        for user in users:
            value = user.to_dict()
            user_data.append(value)
    else:
        for user in users:
            value = user.to_dict()
            if value['clinicCategory'] == category:
                user_data.append(value)

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

        
    return render(request,'index_search.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
    })

def forgot_password(request):
    try:
        if request.method == 'POST':
            forgot_pass_email = request.POST.get('forgot_pass_email')
            auth.send_password_reset_email(forgot_pass_email)
            data = {
                'success': "Successfully Sent To Your Email",
            }
        else:
            data = {
                'success': "",
            }
    except:
        data = {
                'success': "Email Not Found!",
            }

    return render(request,'forgot_password.html', data)


def about(request):
    request.session['session'] = "about"
    return render(request,'about.html',{"session":request.session['session']})

def addAppointment(request):
    if request.method == 'POST': 
        clinic_id = request.POST.get('clinic_id_appointment')

        appointment_name = request.POST.get('appointment_name')
        appointment_email = request.POST.get('appointment_email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        appointment_number = request.POST.get('appointment_number')

        t = time.strptime(appointment_time, "%H:%M")
        timevalue_12hour = time.strftime( "%I:%M %p", t )

        doc_ref = firestoreDB.collection('appointment_queue').document()
        doc_ref.set({
            'user_id': clinic_id,
            'appointment_name' : appointment_name,
            'appointment_email' : appointment_email,
            'appointment_date': appointment_date,
            'appointment_time': timevalue_12hour,
            'appointment_number': appointment_number,
            'appointment_id': doc_ref.id
        })

        email_message = 'Hello Mr./Mrs. '+ appointment_name.upper() +',\n'+ '\nYour Appoinment Request is now Being Processed, Please wait for further notice if Your Request Has Been Accepted or Rejected.\n\nBest Regards,\nGoVet'

        send_mail(
            'Appointment Request',
            email_message,
            'clinic.directory.2021@gmail.com',
            [appointment_email],
            fail_silently=False,
        )

        return redirect('/')

def appointment(request):
    request.session['session'] = "request"
    if 'user_id' in request.session:
        appointment_queue = firestoreDB.collection('appointment_queue').where('user_id' , '==', request.session['user_id']).stream()

        accepted_appointment = firestoreDB.collection('accepted_appointment').where('user_id' , '==', request.session['user_id']).stream()

        queue = []
        accepted = []

        

        for appointment in appointment_queue:
            value = appointment.to_dict()
            queue.append(value)

        for accep in accepted_appointment:
            value = accep.to_dict()
            accepted.append(value)

        paginator = Paginator(queue, 3)
        page_number = request.GET.get('page') or 1
        item_list = paginator.get_page(page_number)

        paginator2 = Paginator(accepted, 3)
        page_number2 = request.GET.get('page2') or 1
        item_list2 = paginator2.get_page(page_number2)

        data ={
            'appointment_queue': queue,
            'accepted_appointment': accepted,
            'session': request.session['session'],
            'item_list': item_list,
            'item_list2': item_list2,
        }

        return render(request, 'appointment.html', data)
    else:
        return redirect('/login')
    
def acceptAppointment(request):
    if request.method == 'POST': 

        clinic_id = request.POST.get('clinic_id')

        appointment_id = request.POST.get('appointment_id')

        appointment_name = request.POST.get('name')
        appointment_email = request.POST.get('email')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        appointment_number = request.POST.get('number')

        doc_ref = firestoreDB.collection('accepted_appointment').document()
        doc_ref.set({
            'user_id': clinic_id,
            'appointment_name' : appointment_name,
            'appointment_email' : appointment_email,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'appointment_number': appointment_number,
            'accepted_appointment_id': doc_ref.id
        })

        email_message = 'Hello Mr./Mrs. '+ appointment_name.upper() +',\n'+ '\nWe would like to inform you that your request to Book an Appoinment Schedule to the ' + request.session['clinic_name'].upper() + ' at ' + appointment_date + ' ' + appointment_time + ' has been ACCEPTED. Please keep this message as proof of acknowledgement from the system for future purposes.\n\nBest Regards,\nGoVet'

        send_mail(
            'Appointment Request',
            email_message,
            'clinic.directory.2021@gmail.com',
            [appointment_email],
            fail_silently=False,
        )

        firestoreDB.collection('appointment_queue').document(appointment_id).delete()

        return redirect('/appointment')

def declineAppointment(request):
    if request.method == 'POST': 
        appointment_id = request.POST.get('appointment_id')

        appointment_name = request.POST.get('name')
        appointment_email = request.POST.get('email')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        reasons = request.POST.get('reasons')

        firestoreDB.collection('appointment_queue').document(appointment_id).delete()

        email_message = 'Hello Mr./Mrs. '+ appointment_name.upper() +',\n'+  '\nWe would like to inform you that your request to Book an Appoinment Schedule to the ' + request.session['clinic_name'].upper() + ' at ' + appointment_date + ' ' + appointment_time + ' has been DECLINED Because of the following reason/reasons:\n' + reasons.upper() + '\nYou Can try Again to Book an Appointment by visiting us at govet.herokuapp.com, Please keep this message as proof of acknowledgement from the system for future purposes.\n\nBest Regards,\nGoVet'

        send_mail(
            'Appointment Request',
            email_message,
            'clinic.directory.2021@gmail.com',
            [appointment_email],
            fail_silently=False,
        )

        return redirect('/appointment')

def delete_appointment(request):
    if request.method == 'GET': 
        appointment_id = request.GET.get('appointment_id')
        firestoreDB.collection('accepted_appointment').document(appointment_id).delete()
        return redirect('/appointment')
    
def grooming(request):
    request.session['grooming'] = "grooming"
    return render(request,'grooming.html',{"session":request.session['grooming']})

def showVetClinics(request):
    #map Size
    request.session['session'] = "dashboard"
    f = folium.Figure(width=880, height=700)

    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

    timeNow = datetime.datetime.now().time()
    date_time = timeNow.strftime('%I:%M %p')
    currentTime = datetime.datetime.strptime(date_time, '%I:%M %p').time()

    users = firestoreDB.collection('users').get()

    user_data = []

    for user in users:
        value = user.to_dict()

        opening_time = datetime.datetime.strptime(value['opening_time'], '%I:%M %p').time()

        closing_time = datetime.datetime.strptime(value['closing_time'], '%I:%M %p').time()

        # opening_time = value['opening_time'].strftime('%I:%M %p')

        # closing_time = value['closing_time'].strftime('%I:%M %p')

        if opening_time < currentTime and currentTime < closing_time:
            value['isOpen'] = "True"
            # user_data.append(value)
        if value['clinicCategory'] == 'Vet Clinic':
            user_data.append(value)

            latitude = value['latitude']
            longitude = value['longitude']
            # commented line removed 5 star image +"<br><br><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><br>5.0" 
            folium.Marker([latitude, longitude], 
            popup= "<img style=\"width:200px;\" src=\""+value['clinic_img_url']+"\">"
            +"<b>Clinic Name:</b><br>" + value['clinic_name'] + "<br><br><b>Clinic Address:</b><br>" 
            + value['clinic_address']  +
            "<br><br><b>Open and Closing time:</b><br>" + value['opening_time'] +
            " - " + value['closing_time'] + "<br><br><em>Description:</em><br>"+
            value['clinic_description']  +"<br><br><b>Contact number:</b><br>" +
                value['clinic_contact_number'] , 
            icon=folium.Icon(color="red", icon="fa-paw", prefix='fa'),
            tooltip= value['clinic_name']).add_to(map)
        

    paginator = Paginator(user_data, 3)
    page_number = request.GET.get('page') or 1
    item_list = paginator.get_page(page_number)
    
    # Get html representation of the map
    map = map._repr_html_()

    if request.method == 'POST':
        userId = request.POST.get('user_id_post')
        items = firestoreDB.collection('items').document(userId).get()

        data = {
            'map': map,
            'user_data': user_data,
            'item_data': items.to_dict(),
         }
        return render(request, 'item_data.html', {'item_data':items.to_dict()})
        #return HttpResponse(json.dumps(items.to_dict()))
    else:
        data = {
            'map': map,
            'user_data': user_data,
            "session":request.session['session'],
            'currentTime': currentTime, 
            'opening_time': opening_time,
            'closing_time': closing_time,
            'item_list':item_list,
            'category': 'Vet Clinic',
            'categoryLabel': 'Vet Clinics',
        }
    
    if 'user_id' not in request.session:
        return render(request,'index.html', data)
    else:
        return redirect('/homepage')


def showPetShops(request):
    #map Size
    request.session['session'] = "dashboard"
    f = folium.Figure(width=880, height=700)

    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

    timeNow = datetime.datetime.now().time()
    date_time = timeNow.strftime('%I:%M %p')
    currentTime = datetime.datetime.strptime(date_time, '%I:%M %p').time()

    users = firestoreDB.collection('users').get()

    user_data = []

    for user in users:
        value = user.to_dict()

        opening_time = datetime.datetime.strptime(value['opening_time'], '%I:%M %p').time()

        closing_time = datetime.datetime.strptime(value['closing_time'], '%I:%M %p').time()

        # opening_time = value['opening_time'].strftime('%I:%M %p')

        # closing_time = value['closing_time'].strftime('%I:%M %p')

        if opening_time < currentTime and currentTime < closing_time:
            value['isOpen'] = "True"
            # user_data.append(value)
        if value['clinicCategory'] == 'Pet Shop':
            user_data.append(value)

            latitude = value['latitude']
            longitude = value['longitude']
            # commented line removed 5 star image +"<br><br><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><br>5.0" 
            folium.Marker([latitude, longitude], 
            popup= "<img style=\"width:200px;\" src=\""+value['clinic_img_url']+"\">"
            +"<b>Clinic Name:</b><br>" + value['clinic_name'] + "<br><br><b>Clinic Address:</b><br>" 
            + value['clinic_address']  +
            "<br><br><b>Open and Closing time:</b><br>" + value['opening_time'] +
            " - " + value['closing_time'] + "<br><br><em>Description:</em><br>"+
            value['clinic_description']  +"<br><br><b>Contact number:</b><br>" +
                value['clinic_contact_number'] , 
            icon=folium.Icon(color="red", icon="fa-paw", prefix='fa'),
            tooltip= value['clinic_name']).add_to(map)
        

    paginator = Paginator(user_data, 3)
    page_number = request.GET.get('page') or 1
    item_list = paginator.get_page(page_number)
    
    # Get html representation of the map
    map = map._repr_html_()

    if request.method == 'POST':
        userId = request.POST.get('user_id_post')
        items = firestoreDB.collection('items').document(userId).get()

        data = {
            'map': map,
            'user_data': user_data,
            'item_data': items.to_dict(),
         }
        return render(request, 'item_data.html', {'item_data':items.to_dict()})
        #return HttpResponse(json.dumps(items.to_dict()))
    else:
        data = {
            'map': map,
            'user_data': user_data,
            "session":request.session['session'],
            'currentTime': currentTime, 
            'opening_time': opening_time,
            'closing_time': closing_time,
            'item_list':item_list,
            'category': 'Pet Shop',
            'categoryLabel': 'Pet Shop',
        }
    
    if 'user_id' not in request.session:
        return render(request,'index.html', data)
    else:
        return redirect('/homepage')

def showPetSalons(request):
    #map Size
    request.session['session'] = "dashboard"
    f = folium.Figure(width=880, height=700)

    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

    timeNow = datetime.datetime.now().time()
    date_time = timeNow.strftime('%I:%M %p')
    currentTime = datetime.datetime.strptime(date_time, '%I:%M %p').time()

    users = firestoreDB.collection('users').get()

    user_data = []

    for user in users:
        value = user.to_dict()

        opening_time = datetime.datetime.strptime(value['opening_time'], '%I:%M %p').time()

        closing_time = datetime.datetime.strptime(value['closing_time'], '%I:%M %p').time()

        # opening_time = value['opening_time'].strftime('%I:%M %p')

        # closing_time = value['closing_time'].strftime('%I:%M %p')

        if opening_time < currentTime and currentTime < closing_time:
            value['isOpen'] = "True"
            # user_data.append(value)
        if value['clinicCategory'] == 'Pet Salon':
            user_data.append(value)

            latitude = value['latitude']
            longitude = value['longitude']
            # commented line removed 5 star image +"<br><br><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><br>5.0" 
            folium.Marker([latitude, longitude], 
            popup= "<img style=\"width:200px;\" src=\""+value['clinic_img_url']+"\">"
            +"<b>Clinic Name:</b><br>" + value['clinic_name'] + "<br><br><b>Clinic Address:</b><br>" 
            + value['clinic_address']  +
            "<br><br><b>Open and Closing time:</b><br>" + value['opening_time'] +
            " - " + value['closing_time'] + "<br><br><em>Description:</em><br>"+
            value['clinic_description']  +"<br><br><b>Contact number:</b><br>" +
                value['clinic_contact_number'] , 
            icon=folium.Icon(color="red", icon="fa-paw", prefix='fa'),
            tooltip= value['clinic_name']).add_to(map)
        

    paginator = Paginator(user_data, 3)
    page_number = request.GET.get('page') or 1
    item_list = paginator.get_page(page_number)
    
    # Get html representation of the map
    map = map._repr_html_()

    if request.method == 'POST':
        userId = request.POST.get('user_id_post')
        items = firestoreDB.collection('items').document(userId).get()
        
        data = {
            'map': map,
            'user_data': user_data,
            'item_data': items.to_dict(),
         }
        return render(request, 'item_data.html', {'item_data':items.to_dict()})
        #return HttpResponse(json.dumps(items.to_dict()))
    else:
        data = {
            'map': map,
            'user_data': user_data,
            "session":request.session['session'],
            'currentTime': currentTime, 
            'opening_time': opening_time,
            'closing_time': closing_time,
            'item_list':item_list,
            'category': 'Pet Salon',
            'categoryLabel': 'Pet Salon',
        }
    
    if 'user_id' not in request.session:
        return render(request,'index.html', data)
    else:
        return redirect('/homepage')

def getSearchDataClinic(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_item')

    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        if value['clinicCategory'] == 'Vet Clinic':
            user_data.append(value)
        

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

    return render(request, 'search_suggest.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
        })

def getSearchDataShop(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_item')

    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        if value['clinicCategory'] == 'Pet Shop':
            user_data.append(value)
        

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

    return render(request, 'search_suggest.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
        })

def getSearchDataSalon(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_item')

    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        if value['clinicCategory'] == 'Pet Salon':
            user_data.append(value)
        

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

    return render(request, 'search_suggest.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
        })