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
    path('payment_info', views.payment_info, name = "payment_info"),
    path('message', views.messagePage, name = "message"),
    path('getMessage', views.getMessages, name = "message"),
    path('operations/', views.tasksview, name = "operations"),
    path('task_detail/<int:id>/', views.taskdetailview, name = "task_detail"),
    ]