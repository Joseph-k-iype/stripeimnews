from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='subscriptions-home'),
    path('home', views.home, name='subscriptions-home'),
    path('config/', views.stripe_config),  # new
    path('create-checkout-session/', views.create_checkout_session),  # new
    path('success/', views.success),  # new
    path('cancel/', views.cancel),  # new
    path('webhook/', views.stripe_webhook),  # new
    path('application/', views.application, name = "application_form"),
    path('postform/', views.postform, name = "postform"),
    path('response/', views.send_email, name = "response"),
    path('payment_info', views.payment_info, name = "payment_info"),
    path('message', views.message_page, name = "message"),
    path('sendMessage', views.sendMessage, name = "message"),
    ]