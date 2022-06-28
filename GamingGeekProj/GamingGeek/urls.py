from django.contrib import admin
from django.urls import path
from django.conf import settings

from . import userControlFuncions as usrFunc
from . import views as views


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    # Navigation the site
    path('', views.home, name='index'),
    path('storehome/', views.MainPage, name='storeHome'),
    path('about/', views.about, name='about'),
    path('editUsers/', views.editUsers, name='editUsers'),

    # Create and deail with users
    path('loginRequest/', usrFunc.login, name='login'),
    path('addNewUser/', usrFunc.addNewUser, name='addNewUser'),
    path('register/', usrFunc.register, name='register'),

    # Function and work
    path('addItems/', views.addItems, name='addItems'),
    path('InsertNewItems/', views.InsertNewItems, name='InsertNewItems'),
    path('editStore/', views.editStore, name='editStore'),
    path('updateItem/', views.updateAnItem, name='updateItem'),
    path('updateUser/', views.updateUser, name='updateUser'),

    # Image uploading
    path('upload/', views.upload, name="upload"),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)