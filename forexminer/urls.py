from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/create-user', views.create_user),  
    path('user/login-user', views.Login_user),  
    path('user/update-account', views.update_account),
    path('user/update-password', views.update_password), 
    path('user/search-role', views.get_account_id_role), 
    path('user/search-id', views.get_account_by_id),  
    path('user/forget-password',views.generate_random_password),
    
    path('admins/create-faq', views.create_FaQ),
    path('admins/update-faq', views.update_FaQs),
    path('admins/search-faq-id', views.get_FaQ_by_id),
    path('admins/delete-faq', views.delete_FaQ),
    path('admins/get-all-faqs', views.get_all_FaQs),
    
    
    path('admins/create-plan', views.create_Plan),
    path('admins/update-plan', views.update_Plan),
    path('admins/delete-plan', views.delete_Plan),
    path('admins/get-all-plan', views.get_all_plans),
    
    path('admins/get-all-feedback', views.get_all_feedbacks),
    path('admins/delete-feedback', views.delete_feedback),
    path('admins/delete-subscriber', views.delete_subscriber),

    path('admins/update-read', views.update_read),
    path('admins/get-all-subscribers', views.get_subscribers),
    path('admins/update-Subscriber', views.update_subscriber),
    path('admins/send-mail', views.send_mail_view),
    path('admins/update-status', views.update_status),

    path('feedback/create-query', views.create_feedback),
    path('admins/get-all-unreaded-feedback',views.get_unread_feedback),
    path('api/stripe/create-checkout-session', views.StripeCheckoutView.as_view()),
    path('get-sessionId', views.get_sessionId),
    path('get-free-subscription', views.get_free_subscription),


    path('feedback/count-feed', views.feedback_count_view),
    path('admins/count-subscribers', views.subscriber_count_view),
    path('admins/total-revenue', views.total_revenue_view),
    path('admins/subscriber-per-month', views.subscriber_count_by_month_view),
    path('admins/subscriber-by-plan', views.subscribers_by_plan_type_view),
    # path('just-testing', views.just_testing),
    


]
