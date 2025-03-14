
from django.contrib import admin
from django.urls import path,include

from multibillionapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('starter/', views.starter, name='starter'),
    path('blog/', views.blog, name='blog'),
    path('services/', views.services, name='services'),
    path('servicedetails/', views.servicedetails, name='servicedetails'),
    path('index/', views.index, name='index'),
    path('blogdetails/', views.blogdetails, name='blogdetails'),
    path('project/', views.project, name='project'),
    path('projectdetails/', views.projectdetails, name='projectdetails'),
    path('appointment/', views.appointment1, name='appointment'),
    path('contact/', views.contact1, name='contact'),
    path('show/', views.show, name='show'),
    path('delete/<int:id>', views.delete),

    path('edit/<int:id>', views.edit, name='edit'),
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    # Mpesa Api
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('transactions/', views.transactions_list, name='transactions'),

]
