from datetime import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json  
from forexminer.models import CustomUser, FaQs
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import random
import string
import smtplib
from .models import CustomUser, Plans, Subscriber
from django.utils import timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


#import pyrebase
from pymongo import MongoClient
client = MongoClient('mongodb+srv://i200867:vj617cultus@cluster0.n7ix9pn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['ForexMiner']


config = {

    "apiKey": "AIzaSyBtQhTIdj5W5ymQHtH4YUFc8Wmt20K3OFY",
    "authDomain": "forexminer-a68e0.firebaseapp.com",
    "databaseURL": "https://forexminer-a68e0-default-rtdb.firebaseio.com",
    "projectId": "forexminer-a68e0",
    "storageBucket": "forexminer-a68e0.appspot.com",
    "messagingSenderId": "364153606890",
    "appId": "1:364153606890:web:c4f7d505f5c81de4b8fd93"

}

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()


from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import random

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            # Check if required fields are provided
            required_fields = ['displayName', 'UserName', 'password', 'email']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

            # Check if email already exists
            email_exists = CustomUser.objects.filter(email=data.get('email'))
            if email_exists:
                return JsonResponse({'error': 'Email already exists'}, status=400)

            # Generate a random 4-digit user ID
            user_id_1 = ''.join(random.choices('0123456789', k=4))

            # Create a new user
            user = CustomUser(
                username=data.get('UserName'),
                password=data.get('password'),
                email=data.get('email'),
                role=data.get('role', 'subscriber'),  # Providing default value for role
                name=data.get('displayName', ''),    # Providing default value for name
                user_id=user_id_1,                    # Providing default value for user_id
                photo_url=data.get('photo_url', '')   # Providing default value for photo_url
            )
            
            user.save()
            
            return JsonResponse({'message': 'User created successfully'})

        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)
        except Exception as e:
            print(f'Error occurred during user creation: {str(e)}')
            return JsonResponse({'error': f'Error occurred during user creation: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


from django.http import JsonResponse
import json
from .models import CustomUser, Plans, Subscriber
from django.core.serializers import serialize


@csrf_exempt
def update_account(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get the user_id from the data
            user_id = data.get('user_id')

            # Check if the user with the provided user_id exists
            try:
                user = CustomUser.objects.get(user_id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=404)

            # Update the user's information
            user.username = data.get('username', user.username)
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role)
            user.photo_url = data.get('photo_url', user.photo_url)
            user.password = data.get('password',user.password)
            user.save()

            serialized_user = serialize('json', [user])

            return JsonResponse({'message': 'User updated successfully', 'user': serialized_user})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.http import JsonResponse
import json
from django.contrib.auth.hashers import check_password
from .models import CustomUser

from django.http import JsonResponse
import json
from .models import CustomUser

@csrf_exempt
def update_password(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get the user_id, current password, and new password from the data
            user_id = data.get('user_id')
            current_password = data.get('password')
            new_password = data.get('newPassword')
            print("data",user_id)
            print("data",current_password)
            print("data",new_password)

            # Check if the user with the provided user_id exists
            try:
                user = CustomUser.objects.get(user_id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=404)

            # Check if the provided current password matches the user's actual password
            if current_password != user.password:
                return JsonResponse({'error': 'Incorrect current password'}, status=409)

            # Update the user's password
            user.password = new_password
            user.save()

            # You may choose to return a response with updated user information
            # Or return a simple success message
            return JsonResponse({'message': 'Password updated successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

import string
@csrf_exempt
def generate_random_password(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get the user_id, current password, and new password from the data
            email = data.get('email')

            # Check if the user with the provided user_id exists
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Email does not exist'}, status=404)
            
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(random.choices(characters, k=8))

            # Update the user's password
            user.password = new_password
            
            subject = "Your New Password"
            message = (
                f"Hi {user.name},\n\n"
                "Thank you for contacting Forex Miner. As requested, we have generated a new password for your account.\n\n"
                f"Your new password is: {new_password}\n\n"
                "Please make sure to change this password once you log in and keep your credentials secure.\n\n"
                "Best regards,\n"
                "Team Forex Miner"
            )

            # Send the email
            try:
                smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                smtpserver.starttls()
                smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

                msg = f'Subject: {subject}\n\n{message}'
                smtpserver.sendmail(
                    settings.EMAIL_HOST_USER,
                    email,
                    msg
                )
                smtpserver.quit()
                user.save()
                return JsonResponse({'message': 'New Password created successfully'})

            except Exception as e:
                        return JsonResponse({'success': False, 'message': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.views.decorators.csrf import csrf_protect


@csrf_exempt
def get_account_id_role(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get role from the data
            role = data.get('role')
            print("Role:", role)

            # Check if role is empty or undefined
            if not role:
                return JsonResponse({'error': 'Role is not defined'}, status=400)

            # Search for users based on role
            users = CustomUser.objects.filter(role=role)

            if not users:
                return JsonResponse({'error': 'No users found'}, status=404)

            # Prepare data for response
            user_data = []
            for user in users:
                user_info = {
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'password': user.password,
                    'role': user.role,
                    'photo_url': user.photo_url
                }
                user_data.append(user_info)

            # Return response with user data
            return JsonResponse({'users': user_data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


from django.views.decorators.csrf import csrf_protect
@csrf_exempt
def get_account_by_id(request):
  if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get role from the data
            user_id = data

            # Check if role is empty or undefined
            if not user_id:
                return JsonResponse({'error': 'User_Id is empty or undefined'}, status=400)

            # Search for users based on role
            users = CustomUser.objects.filter(user_id=user_id)

            if not users:
                return JsonResponse({'error': 'No users found with the specified ID'}, status=404)

            # Prepare data for response
            user_data = []
            for user in users:
                user_info = {
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'password': user.password,
                    'role': user.role
                }
                user_data.append(user_info)

            # Return response with user data
            return JsonResponse({'users': user_data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

from django.core.serializers import serialize
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect

@csrf_exempt
def Login_user(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            # Retrieve user based on email
            email = data.get('email')
            role = data.get('role')

            # Retrieve user from the database based on email and role
            try:
                user = CustomUser.objects.get(email=email, role=role)
                serialized_user = serialize('json', [user])
                
                # Retrieve the most recent subscriber record for the user
                try:
                    subscriber = Subscriber.objects.filter(user=user).latest('date')
                    print(subscriber.date)
                    subscriber_data = {
                        'plan': subscriber.plan.Plan_Title,
                        'account_type': subscriber.plan.AccountType,
                        'date': subscriber.date,
                        'status': subscriber.status,
                    }
                except Subscriber.DoesNotExist:
                    subscriber_data = None

            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

            # Check if password matches
            if data.get('password') == user.password:
                response_data = {
                    'message': 'User logged in successfully',
                    'user': serialized_user,
                    'subscriber': subscriber_data
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

import random

@csrf_exempt
def create_FaQ(request):
     if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            FAQ_id_1 = ''.join(random.choices('0123456789', k=4))
            print(data)
            # Check if required fields are provided
            required_fields = ['question', 'answer']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)
            
            # Check if FAQ already exists
            if FaQs.objects.filter(Questions=data['question']).exists():
                return JsonResponse({'error': 'Question already exists'}, status=400)

            # Create a new FAQ
            faq = FaQs(
                Questions=data['question'],
                Answers=data['answer'],
                FaQ_id = FAQ_id_1,

            )
            faq.save()

            return JsonResponse({'message': 'FAQ created successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
   

from django.views.decorators.csrf import csrf_protect

@csrf_exempt
def update_FaQs(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get the FAQ_id from the data
            FaQ_id = data.get('id')

            # Check if the FAQ with the provided FaQ_id exists
            if FaQ_id is None:
                return JsonResponse({'error': 'FAQ id is required'}, status=400)

            try:
                faq = FaQs.objects.get(FaQ_id=FaQ_id)
            except FaQs.DoesNotExist:
                return JsonResponse({'error': 'FAQ does not exist'}, status=404)

            # Update the FAQ's information
            faq.Questions = data.get('question', faq.Questions)
            faq.Answers = data.get('answer', faq.Answers)
            faq.save()

            return JsonResponse({'message': 'FAQ updated successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


from django.core import serializers

from django.views.decorators.csrf import csrf_protect
@csrf_exempt
def get_FaQ_by_id(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            # Get faq_id from the data
            FaQ_id = data
            
            print(FaQ_id)
 
            # Check if faq is provided
            if not FaQ_id:
                return JsonResponse({'error': 'FAQ ID is required'}, status=400)

            # Search for faq based on user_id
            try:
                faq = FaQs.objects.get(FaQ_id=FaQ_id)
                # Serialize the FAQ object to JSON
                faq_json = serializers.serialize('json', [faq])
                # Convert the serialized JSON to a Python dictionary
                faq_data = json.loads(faq_json)
                # Return the found FAQ object
                return JsonResponse({'message': 'FAQ found with the specified ID', 'faq': faq_data[0]})
            except FaQs.DoesNotExist:
                return JsonResponse({'error': 'FAQ not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_all_FaQs(request):
    if request.method == 'GET':
        try:
            # Retrieve all FAQs from the database
            faqs = FaQs.objects.all()
            # Convert the queryset to a list of dictionaries
            faqs_list = [{'FaQ_id': faq.FaQ_id, 'question': faq.Questions, 'answer': faq.Answers} for faq in faqs]
            
            # Return the list of FAQs
            return JsonResponse({'faqs': faqs_list})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)


from django.views.decorators.csrf import csrf_protect

@csrf_exempt
def delete_FaQ(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # Check if FAQ ID is provided
            faq_id = data.get("FaQ_id")  # Access FaQ_id from data

            if not faq_id:
                return JsonResponse({'error': 'FAQ ID is required'}, status=400)

            # Check if FAQ with the provided ID exists
            try:
                faq = FaQs.objects.get(FaQ_id=faq_id)
            except FaQs.DoesNotExist:
                return JsonResponse({'error': 'FAQ not found'}, status=404)

            faq.delete()

            return JsonResponse({'message': 'FAQ deleted successfully'}, status=200)

        except Exception as e:
            # Print the exception for debugging purposes
            return JsonResponse({'error': str(e)}, status=400)


from django.views.decorators.csrf import csrf_protect

@csrf_exempt    
def delete_Plan(request):
    if request.method == 'DELETE':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            # Check if Plan ID is provided
            Plan_id = data.get('Plan_id')
            if not Plan_id:
                return JsonResponse({'error': 'Plan ID is required'}, status=400)

            # Check if Plan with the provided ID exists
            try:
                plan = Plans.objects.get(Plan_id=Plan_id)
            except Plans.DoesNotExist:
                return JsonResponse({'error': 'Plan not found'}, status=404)

            # Delete the FAQ
            plan.delete()

            return JsonResponse({'message': 'Plan deleted successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



from django.views.decorators.csrf import csrf_protect

@csrf_exempt
def update_Plan(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Get the Plan_id from the data
            Plan_id = data.get('id')

            # Check if the plan with the provided Plan_id exists
            try:
                plan = Plans.objects.get(Plan_id=Plan_id)
            except Plans.DoesNotExist:
                return JsonResponse({'error': 'Plan does not exist'}, status=404)

            # Update the plan's information
            plan.Plan_Title = data.get('title', plan.Plan_Title)
            plan.Plan_subHeader = data.get('subtitle', plan.Plan_subHeader)
            plan.Plan_Price = data.get('price', plan.Plan_Price)
            plan.AccountType = data.get('accountType', plan.AccountType)
            plan.Plan_Feature = data.get('description', plan.Plan_Feature)
            plan.save()

            return JsonResponse({'message': 'Plan updated successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
def create_Plan(request):
    if request.method == 'POST':
        try:
            # Get the data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))
            Plan_id_1 = ''.join(random.choices('0123456789', k=4))
            print(data)

            # Check if required fields are provided
            required_fields = ['title', 'subTitle', 'price', 'accountType', 'description']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'{field.capitalize()} is required'}, status=400)

            # Create a new Plan
            plan = Plans(
                Plan_Title=data['title'],
                Plan_subHeader=data['subTitle'],
                Plan_Price=data['price'],
                AccountType=data['accountType'],
                Plan_Feature=data['description'],
                Plan_id=Plan_id_1
            )
            plan.save()

            return JsonResponse({'message': 'Plans created successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def get_all_plans(request):
    if request.method == 'GET':
        try:
            # Retrieve all plans from the database
            plans = Plans.objects.all()

            # Convert the queryset to a list of dictionaries
            plans_list = []
            for plan in plans:
                plan_dict = {
                    'Plan_id': plan.Plan_id,
                    'Plan_Title': plan.Plan_Title,
                    'Plan_subHeader': plan.Plan_subHeader,
                    'Plan_Price': plan.Plan_Price,
                    'AccountType': plan.AccountType,
                    'Plan_Feature': plan.Plan_Feature, 
                    'created_by': plan.created_by.username if plan.created_by else None
                }
                plans_list.append(plan_dict)

            # Return the list of plans
            return JsonResponse({'plans': plans_list}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)


import json
import random
import pytz
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Feedback, Plans, Subscriber, CustomUser

@csrf_exempt
def create_feedback(request):
    if request.method == 'POST':
        try:
            # Parse data from the POST request's body
            data = json.loads(request.body.decode('utf-8'))

            # Extract necessary fields from the data
            sender_name = data.get('sender_name')
            sender_email = data.get('sender_email')
            subject = data.get('subject')
            message = data.get('message')
            feedback_type = data.get('feedback_type')
            
            print(sender_email)
            query_id_1 = ''.join(random.choices('0123456789', k=4))
            # Check if email is present in the database
            try:
                receiver_user = CustomUser.objects.get(email=sender_email)
                print(receiver_user)
                receiver_id = receiver_user.user_id
            except CustomUser.DoesNotExist:
                # If email is not found in the database, set receiver_id to None
                return JsonResponse({"message": "Email doesn't exist"}, status=400)

            # Create the feedback
            feedback = Feedback.objects.create(
                sender_id=receiver_id,  # Storing sender email as sender_id
                subject=subject,
                message=message,
                query_id = query_id_1,
                feedback_type = feedback_type,   
            )

            feedback.save()

            # Return success response
            return JsonResponse({'message': 'Feedback created successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'},status=405)


from django.http import JsonResponse
from django.utils.timesince import timesince
from .models import Feedback, CustomUser
from datetime import datetime  # Import datetime module

@csrf_exempt
def get_unread_feedback(request):
    if request.method == 'GET':
        try:
            # Retrieve all feedbacks where status is 'not responded' and read is False
            unread_feedbacks = Feedback.objects.all()
            
            # Prepare the response data
            feedbacks_list = []
            for feedback in unread_feedbacks:
                # Debugging: Print sender_id to verify it's correct
                print("Sender ID:", feedback.sender_id)
                
                # Get the name of the sender using the sender_id
                sender = CustomUser.objects.filter(user_id=feedback.sender_id).first()
                
                # Debugging: Print sender object to see if it's retrieved
                print("Sender Object:", sender)
                
                sender_name = sender.name if sender else "Unknown User"

                # Calculate the time elapsed since feedback creation
                created_at = feedback.created_at
                time_since_creation = format_time_since(timesince(created_at))  # Convert timedelta to string

                # Create a dictionary for the feedback
                feedback_dict = {
                    'id': feedback.query_id,
                    'sender_name': sender_name,
                    'subject': feedback.subject,
                    'message': feedback.message,
                    'read': feedback.read,
                    'time_since_creation': time_since_creation
                }
                feedbacks_list.append(feedback_dict)

            # Return the list of unread feedbacks as a JSON response
            return JsonResponse({'feedbacks': feedbacks_list}, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Include the exception message in the response
    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)

def format_time_since(time_since):
    if 'year' in time_since:
        return time_since.replace(',', '')
    elif 'month' in time_since:
        return time_since.replace(',', '')
    elif 'week' in time_since:
        return time_since.replace(',', '')
    elif 'day' in time_since:
        return time_since.replace(',', '')
    elif 'hour' in time_since:
        return time_since.replace(',', '')
    elif 'minute' in time_since:
        return time_since.replace(',', '')
    else:
        return 'Just now'


def get_all_feedbacks(request):
    if request.method == 'GET':
        try:
            # Retrieve all feedbacks from the database
            feedbacks = Feedback.objects.all()

            # Prepare the response data
            feedbacks_list = []
            for feedback in feedbacks:
                # Fetch sender details based on sender_id
                sender = CustomUser.objects.filter(user_id=feedback.sender_id).first()
                sender_name = sender.name if sender else None
                sender_email = sender.email if sender else None

                feedback_dict = {
                    'query_id': feedback.query_id,
                    'sender_id': feedback.sender_id,
                    'sender_name': sender_name,
                    'sender_email': sender_email,
                    'subject': feedback.subject,
                    'message': feedback.message,
                    'feedback_type': feedback.feedback_type,
                    'read': feedback.read,
                    'status': feedback.status,
                    'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format date as string
                }
                feedbacks_list.append(feedback_dict)

            # Return the list of feedbacks as a JSON response
            return JsonResponse({'feedbacks': feedbacks_list}, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only GET requests are supported'},status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback

@csrf_exempt
def update_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # Get the notification ID and read status from the request data
            notification_id = data.get('id')
            read_status = data.get('read')
            print("Notification",notification_id)
            print("Notification",read_status)
            # Find the notification object based on the ID
            notification = Feedback.objects.get(query_id=notification_id)
            
            # Update the read status
            notification.read = read_status
            notification.save()
            
            # Return a success response
            return JsonResponse({'message': 'Notification read status updated successfully'}, status=200)
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Notification not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
def delete_feedback(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body.decode('utf-8'))
            query_id = data.get('query_id')  # Access query_id from the data dictionary
            print(query_id)
            feedback = Feedback.objects.get(query_id=query_id)

            # Delete the feedback
            feedback.delete()

            # Return success response
            return JsonResponse({'message': 'Feedback deleted successfully'})

        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Feedback not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only DELETE requests are supported'}, status=405)


def get_subscribers(request):
    if request.method == 'GET':
        try:
            # Retrieve all subscriber records from the database
            subscribers = Subscriber.objects.all()

            # Prepare response data
            subscribers_list = []
            for subscriber in subscribers:
                # Extract relevant information from associated models
                account_type = subscriber.plan.AccountType
                name = subscriber.user.name
                username = subscriber.user.username
                email = subscriber.user.email
                password = subscriber.user.password  # Note: Password retrieval should be handled securely
                date = subscriber.date
                status = subscriber.status

                # Construct subscriber record dictionary
                subscriber_record = {
                    'id': subscriber.Subscriber_id,
                    'accountType': account_type,
                    'name': name,
                    'username': username,
                    'email': email,
                    'password': password,  # Note: Password should be handled securely
                    'paymentDate': date,
                    'paymentStatus': status
                }
                # Append subscriber record to the list
                subscribers_list.append(subscriber_record)

            # Return the list of subscriber records as a JSON response
            return JsonResponse({'subscribers': subscribers_list}, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only GET requests are supported'}, status=405)


import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def update_subscriber(request):
    if request.method == 'POST':
        try:
            # Extract data from the request
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            name = data.get('name')
            username = data.get('username')
            password = data.get('password')

            logger.debug(f"Received POST request with data: email={email}, name={name}, password={password}, username={username}")

            # Find the user by email
            user = CustomUser.objects.get(email=email)

            logger.debug(f"Found user with email: {email}")

            # Update subscriber details based on the found user
            subscribers = Subscriber.objects.filter(user=user)
            for subscriber in subscribers:
                subscriber.user.name = name
                subscriber.user.password = password
                subscriber.user.username = username
                subscriber.user.save()

            logger.info("Subscriber details updated successfully")

            return JsonResponse({'message': 'Subscriber details updated successfully'}, status=200)

        except CustomUser.DoesNotExist:
            logger.error("User not found with the provided email")
            return JsonResponse({'error': 'User not found with the provided email'}, status=404)
        except Subscriber.DoesNotExist:
            logger.error("Subscriber not found for the provided email")
            return JsonResponse({'error': 'Subscriber not found for the provided email'}, status=404)
        except Exception as e:
            logger.exception("An error occurred during subscriber update")
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


@csrf_exempt
def delete_subscriber(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body.decode('utf-8'))
            Subscriber_id = data.get('id')  # Access query_id from the data dictionary
            print(Subscriber_id)
            subscriber = Subscriber.objects.get(Subscriber_id=Subscriber_id)

            # Delete the feedback
            subscriber.delete()

            # Return success response
            return JsonResponse({'message': 'Subscriber deleted successfully'})

        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Subscriber not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only DELETE requests are supported'}, status=405)



def feedback_count_view(request):
    if request.method == 'GET':
        # Counting the number of feedbacks in the database
        count = Feedback.objects.count()
        return JsonResponse({'total_feedbacks': count})
    else:
        return JsonResponse({'error': 'GET request required'}, status=400)


def subscriber_count_view(request):
    if request.method == 'GET':
        # Counting the number of feedbacks in the database
        count = Subscriber.objects.count()
        return JsonResponse({'total_subscribers': count})
    else:
        return JsonResponse({'error': 'GET request required'}, status=400)


def total_revenue_view(request):
    if request.method == 'GET':
        # Filter subscribers with status 'paid'
        paid_subscribers_count = Subscriber.objects.filter(status='paid').count()
        # Assuming each paid subscriber contributes $20 to the revenue
        total_revenue = paid_subscribers_count * 20  # $20 per paid subscriber
        return JsonResponse({'total_revenue': f'${total_revenue}'})
    else:
        return JsonResponse({'error': 'GET request required'}, status=400)


def subscribers_by_plan_type_view(request):
    if request.method == 'GET':
        # Assuming '0' and '15' are strings in Plan_Price
        free_count = Subscriber.objects.filter(plan__Plan_Price='0').count()
        paid_count = Subscriber.objects.filter(plan__Plan_Price='20').count()

        return JsonResponse({
            'free_subscribers': free_count,
            'paid_subscribers': paid_count
        })
    else:
        return JsonResponse({'error': 'GET request required'}, status=400)


from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime

def subscriber_count_by_month_view(request):
    if request.method == 'GET':
        try:
            # Retrieve all subscribers
            subscribers = Subscriber.objects.all()

            # Create a dictionary to store monthly subscriber counts
            monthly_subscriber_counts = {}

            # Iterate over each subscriber and count subscribers for each month
            for subscriber in subscribers:
                month = subscriber.date.month
                month_name = datetime.strptime(str(month), "%m").strftime("%B")

                if month_name in monthly_subscriber_counts:
                    monthly_subscriber_counts[month_name] += 1
                else:
                    monthly_subscriber_counts[month_name] = 1

            # Convert the dictionary to the desired format
            chart_data = [
                {'name': month_name, 'user': count}
                for month_name, count in monthly_subscriber_counts.items()
            ]

            return JsonResponse({'chartData': chart_data})
        except Exception as e:
            # Catch any exceptions and return an error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Return a 400 Bad Request response for non-GET requests
        return JsonResponse({'error': 'GET request required'}, status=400)

    
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from forexminer.models import CustomUser

# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import smtplib

        # subject = data.get('subject')
        # message = (f"Hi {user_name}\n"
        #            "Thanks for contacting us.\n\n"
        #            f"Question: {question}\n"
        #            f"Response: {response}\n\n"
        #            "Hope this clears out your query. In case of any ambiguity, do let us know.\n\n"
        #            "Team Forex Miner\n\n")

@csrf_exempt
def send_mail_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        receiver_email = data.get('email')
        name = data.get('name')  # Assuming the user's name is part of the request
        question = data.get('question')  # Assuming the user's question is part of the request
        response = data.get('message')  # Your response to the user's question

        subject = data.get('subject')
        message = (f"Hi {name}\n"
                   "Thanks for contacting us.\n"
                   f"{response}\n"
                   "Hope this will help. In case of any ambiguity, do let us know.\n\n"
                   "Team Forex Miner\n\n")

        try:
            smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtpserver.starttls()
            smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

            msg = f'Subject: {subject}\n\n{message}'
            smtpserver.sendmail(
                settings.EMAIL_HOST_USER,
                receiver_email,
                msg
            )
            smtpserver.quit()

            return JsonResponse({'success': True, 'message': 'Email sent successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)



@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        receiver_email = data.get('sender_email')
        name = data.get('sender_name')  
        question = data.get('message')  
        response = data.get('response')  
        query_id = data.get('query_id')
        subject = data.get('subject')
        message = (f"Hi {name}\n"
                   "Thanks for contacting us.\n"
                   f"Questions: {question}\n"
                   f"{response}\n"
                   "Hope this will help. In case of any ambiguity, do let us know.\n\n"
                   "Team Forex Miner\n\n")

        try:
            smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            smtpserver.starttls()
            smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

            msg = f'Subject: {subject}\n\n{message}'
            smtpserver.sendmail(
                settings.EMAIL_HOST_USER,
                receiver_email,
                msg
            )
            smtpserver.quit()
            # Update the status of the message in the database
            try:
                query = Feedback.objects.get(query_id=query_id)
                query.status = 'responded'
                query.save()
            except Feedback.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Query not found'}, status=404)

            return JsonResponse({'success': True, 'message': 'Email sent successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.conf import settings

import stripe

# Set the API key
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1Owz7mHZ8nntoEdw1lQiYuYp',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],  # Change to payment_method_types
                mode='payment',
                success_url=settings.SITE_URL + '/stripe/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/stripe/success/?canceled=true',
            )
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:   
            # Capture specific Stripe errors
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Capture other exceptions
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

import stripe
from django.http import JsonResponse

# Set your Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.http import JsonResponse
import stripe

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber, Plans
import json
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def get_sessionId(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        session_id = data.get('session_id')
        user_id = data.get('user')

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_status = session.payment_status

            if payment_status == 'paid':
                user = CustomUser.objects.get(user_id=user_id)
                plan = Plans.objects.get(AccountType="Trading")

                if plan:
                    current_datetime = timezone.now()
                    subscriber = Subscriber.objects.create(
                        Subscriber_id=session_id,
                        user=user,
                        plan=plan,
                        status='paid',
                        date=current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    )

                    # Send confirmation email to the user
                    receiver_email = user.email
                    name = user.name
                    subject = "Claim Your Bot Subscription"
                    message = (
                        f"Dear {name},\n\n"
                        "Thank you for subscribing to Forex Miner!\n\n"
                        "We're excited to have you on board.\n\n"
                        "Below is zip folder for Paid Bot Subscription\n\n"
                        "We hope this tool will assist you in trading emotionlessly. Should you have any questions or need assistance, please don't hesitate to reach out to us.\n\n"
                        "Best regards,\n"
                        "Team Forex Miner\n\n"
                    )
                
                    # Path to the existing zip file on the server
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    zip_file_path = os.path.join(base_dir, 'Trading Bot Final.zip')

                    try:
                        # Create the email with an attachment
                        msg = MIMEMultipart()
                        msg['From'] = settings.EMAIL_HOST_USER
                        msg['To'] = receiver_email
                        msg['Subject'] = subject

                        # Attach the message body
                        msg.attach(MIMEText(message, 'plain'))

                        # Attach the zip file
                        with open(zip_file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file_path)}')
                        msg.attach(part)

                        smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                        smtpserver.starttls()
                        smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

                        # Send the MIME email
                        smtpserver.sendmail(
                            settings.EMAIL_HOST_USER,
                            receiver_email,
                            msg.as_string()
                        )
                        smtpserver.quit()

                        return JsonResponse({'success': True,
                                             'message': 'Successfully subscribed to Pro Plan',
                                             "Date": current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                                             "Title": plan.Plan_Title,
                                             "AccountType": plan.AccountType},
                                            status=200)
                    except Exception as e:
                        return JsonResponse({'success': False, 'message': str(e)}, status=500)

                else:
                    return JsonResponse({'success': False, 'message': 'No trading plan found'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Payment not successful'}, status=400)

        except stripe.error.InvalidRequestError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

@csrf_exempt
def get_free_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user')  
        print(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

        # Check if user_id is provided
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User ID is missing'}, status=400)
        
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
        
        try:
            subscriber_id_1 = ''.join(random.choices('0123456789', k=4))

            # Retrieve the plan based on accountType
            plan = Plans.objects.get(AccountType="Demo")
            if plan:
                # Store the successful payment information in your database
                current_datetime = timezone.now()
                subscriber = Subscriber.objects.create(
                    Subscriber_id=subscriber_id_1,
                    user=user,
                    plan=plan,
                    status='none',
                    date=current_datetime.strftime('%Y-%m-%d %H:%M:%S') 
                )
                
                receiver_email = user.email
                name = user.name  
                subject = "Claim Your Bot Subscription"
                message = (
                    f"Dear {name},\n\n"
                    "Thank you for subscribing to Forex Miner!\n\n"
                    "We're excited to have you on board.\n\n"
                    "Below is Folder for Free Bot Subscription\n\n"
                    "We hope this tool will assist you in trading emotionlessly. Should you have any questions or need assistance, please don't hesitate to reach out to us.\n\n"
                    "Best regards,\n"
                    "Team Forex Miner\n\n"
                )
                
                # Path to the existing zip file on the server
                base_dir = os.path.dirname(os.path.abspath(__file__))
                zip_file_path = os.path.join(base_dir, 'Trading Bot Final.zip')

                try:
                    # Create the email with an attachment
                    msg = MIMEMultipart()
                    msg['From'] = settings.EMAIL_HOST_USER
                    msg['To'] = receiver_email
                    msg['Subject'] = subject

                    # Attach the message body
                    msg.attach(MIMEText(message, 'plain'))

                    # Attach the zip file
                    with open(zip_file_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file_path)}')
                    msg.attach(part)

                    smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    smtpserver.starttls()
                    smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_APP_PASSWORD)

                    # Send the MIME email
                    smtpserver.sendmail(
                        settings.EMAIL_HOST_USER,
                        receiver_email,
                        msg.as_string()
                    )
                    smtpserver.quit()
                    subscriber.save()

                    return JsonResponse({
                        'success': True, 
                        'message': 'Successfully subscribed to Free Plan',
                        'date': current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        "Title": plan.Plan_Title, 
                        "AccountType": plan.AccountType
                    }, status=200)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)}, status=500)

            else:
                return JsonResponse({'success': False, 'message': 'No trading plan found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

