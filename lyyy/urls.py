"""lyyy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from attractions import views as viewsa
from users import  views as viewsu

urlpatterns = [
    path('admin/', admin.site.urls,name= 'admin'),
#主页
    path('users/', include('users.urls')),
    path('', viewsa.view_attractions, name='view_attractions'),
    path('home', viewsa.view_attractions, name='view_attractions'),
    path('home/reservation/<int:attraction_id>/', viewsa.get_attraction_detail, name='get_attraction_detail'),
    path('attractions/<str:province_name>/', viewsa.get_attractions_by_province, name='get_attractions_by_province'),
    path('attractions/detail/<int:attraction_id>/', viewsa.get_attraction_detail, name='get_attraction_detail'),
#我的预约
    path('my_reservations/', viewsa.my_reservations_view, name='my_reservations'),
    # 付款单个预约
    path('pay_reservation/<int:reservation_id>/', viewsa.pay_reservation, name='pay_reservation'),
    # 一键付款所有未支付的预约
    path('pay_all_reservations/', viewsa.pay_all_reservations, name='pay_all_reservations'),
    path('payment_success/', viewsa.payment_success, name='payment_success'),

#预约
    path('attractions/submit_review/<int:attraction_id>/', viewsa.submit_review, name='submit_review'),
    path('reserve/<int:attraction_id>/', viewsa.reservation, name='reservation'),  # URL 和视图函数关联
    path('reservation_success/<int:reservation_id>/', viewsa.reservation_success, name='reservation_success'),
#个人信息
    path('profile/', viewsa.profile_view, name='profile'),
#景区管理员
    path('manager_login/', viewsa.manager_login, name='manager_login'),
    path('manager_dashboard/', viewsa.manager_dashboard, name='manager_dashboard'),
    path('approve_reservation/<int:reservation_id>/', viewsa.approve_reservation, name='approve_reservation'),
    path('reject_reservation/<int:reservation_id>/', viewsa.reject_reservation, name='reject_reservation'),
    path('batch_approve_reservations/', viewsa.batch_update_reservations, name='batch_update_reservations'),
]
