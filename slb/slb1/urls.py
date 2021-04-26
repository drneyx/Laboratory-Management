from django.contrib.auth import logout
from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.index, name='index'),

    #authentication
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name="logout"),

    #equipment
    path('equipment/', views.equipment, name="equipment"),
    path('new_equipment/', views.new_equipment, name="new_equipment"),
    path('update_equipment/<int:pk>', views.update_equipment, name="update_equipment"),
    path('delete_equipment/<int:pk>', views.delete_equipment, name="delete_equipment"),


    #students
    path('students/', views.students, name="students"),
    path('student_home/', views.student_home, name="student_home"),
    path('rcart/',views.reserve_summary, name='rcart'),

    #admin
    path('update_item/', views.updateItem, name='updateItem'),
    path('reserved/', views.reserved, name="reserved"),
    path('collection/', views.collection, name="collection"),
    path('approve/<int:pk>', views.approve, name="approve"),
    path('complete/<int:pk>', views.complete_order, name="complete_order"),
    path('collect/<int:pk>', views.collect, name="collect"),
    path('student_approve/<int:pk>', views.student_approve, name="approve_student"),
    
]
