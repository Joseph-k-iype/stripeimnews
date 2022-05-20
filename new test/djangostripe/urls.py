from django.contrib import admin
from django.urls import path, include # new
from django.conf.urls.i18n import i18n_patterns
from subscriptions import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/subscriptions/conversation/', views.showMailListToAdmin),
    path('admin/subscriptions/message/<str:mEmail>/', views.showConvToAdmin),
    path('admin/subscriptions/message/<str:mEmail>/sendMessageFromAdmin', views.sendMessageFromAdmin, name = "message"),
    path('admin/', admin.site.urls),
    path('', include('subscriptions.urls')), # new
    path('accounts/', include('allauth.urls')),  # new
    path("i18n/", include("django.conf.urls.i18n")),    
]

urlpatterns += i18n_patterns(path("admin/", admin.site.urls))
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)