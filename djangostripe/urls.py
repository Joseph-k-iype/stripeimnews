from django.contrib import admin
from django.urls import path, include # new
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('subscriptions.urls')), # new
    path('accounts/', include('allauth.urls')),  # new
    path("i18n/", include("django.conf.urls.i18n")),
    
]

urlpatterns += i18n_patterns(path("admin/", admin.site.urls))