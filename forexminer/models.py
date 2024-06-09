# from typing import List
# from pydantic import BaseModel
# from pydantic import validator


# class User(BaseModel):
#     username: str
#     user_id: str
#     password: str


from django.db import models

class CustomUser(models.Model):
    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'

    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (SUBSCRIBER, 'subscriber'),
    ]
    
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default=SUBSCRIBER)
    username = models.CharField(max_length=100, default='')
    user_id = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    photo_url = models.CharField(max_length=100, default='')

class Meta:
    app_label = 'forexminer'


class FaQs(models.Model):
    FaQ_id = models.CharField(max_length=100) 
    Questions = models.CharField(max_length=100)
    Answers = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

     

class Plans(models.Model):
    Plan_id = models.CharField(max_length=100)
    Plan_Title = models.CharField(max_length=100)  # Add Plan Title field
    Plan_subHeader = models.CharField(max_length=100)  # Add Plan Subheader field
    Plan_Price = models.CharField(max_length=100)
    AccountType = models.CharField(max_length=100)
    Plan_Feature = models.CharField(max_length=100)  # Array for the multiple strings
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)


class Feedback(models.Model):
    query_id = models.CharField(max_length=100)
    sender_id = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    feedback_type = models.CharField(max_length=100, default='feedback')
    reciever_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    read = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='not responded')
    created_at = models.DateTimeField(auto_now_add=True)



class Subscriber(models.Model):
    Subscriber_id = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='paid')









