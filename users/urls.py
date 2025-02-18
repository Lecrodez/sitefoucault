from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)