from django.contrib import admin
from django.urls import path, include # new
from django.conf.urls.i18n import i18n_patterns
from subscriptions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/subscriptions/conversation/', views.showConversationsToAdmin),
    path('admin/subscriptions/conversation/add/', views.newConversation),
    path('admin/subscriptions/message/<str:mEmail>/', views.formMessagePage),
    path('admin/subscriptions/message/<str:mEmail>/getMessages', views.getMessages, name = "message"),
    path('admin/', admin.site.urls),
    path('', include('subscriptions.urls')), # new
    path('accounts/', include('allauth.urls')),  # new
    path("i18n/", include("django.conf.urls.i18n")),    
]

urlpatterns += i18n_patterns(path("admin/", admin.site.urls))
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
#        path('admin/subscriptions/conversation/', views.showMailListToAdmin),

