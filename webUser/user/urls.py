from django.urls import path
from . import views
from login import views as login_views
from history import views as history_views
from payment import views as payment_views
from register import views as register_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', login_views.login_view, name='login'),
    path('history/', history_views.history_view, name='history'),
    path('history/search/', history_views.search_history_ajax, name='search_history_ajax'), 
    path('payment/', payment_views.payment_view, name='payment'),
    path('register/', register_views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('registerVehicle/', register_views.register_vehicle, name='registerVehicle'),
    path('account/', views.account_view, name='account'),
    path('deposit_money/', views.deposit_money, name='deposit_money'), # api nạp tiền bank
    path('payment/vehicle-details/', payment_views.vehicle_details_api, name='vehicle_details_api'), # api lấy thông tin xe
    path('payment/process_parking_payment/', payment_views.process_parking_payment, name='process_parking_payment'), # api xác nhận thanh toán
]