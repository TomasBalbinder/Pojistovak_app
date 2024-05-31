
from django.urls import path
from evidence_pojisteni_app import views


urlpatterns = [
    
    path('', views.index, name='index' ),
    path('about_aplication/', views.about_aplication_view, name='about_aplication'),
    path('list_insured_customers/', views.list_insured_customers, name='list_insured_customers'),
    path('pojistenci/novy/', views.new_insured_view, name='new_insured'),
    path('pojistenci/novy/<int:pk>/', views.new_insured_view, name='edit_insured'),
    path('pojistenci/new_insurance/', views.new_insurance_view, name='new_insurance'),
    path('pojistenci/edit/<int:pk>/', views.edit_insurance_view, name='edit_insurance'),
    path('pojistenci/<int:pk>/', views.insured_detail_view, name='insured_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('users_sales/', views.users_sales_view, name='users_sales'),
    path('pojisteni/smazat/<int:pk>/', views.delete_insurance_view, name='delete_insurance'),
    path('smazat/<int:pk>/', views.delete_customer_view, name='delete_customer'),   
]