

from django.urls import path,include
from . import views
from .views import *



urlpatterns = [
    path('', views.index, name='index'),
    path('',views.apiOverview,name='apiOverview'),
    path('fileupload', FileUploadView.as_view()),
    path('category-list/',views.Showall,name='category-list'),
    path('Showallemployee',views.Showallemployee,name='Showallemployee'),
    path('category-view/<int:pk>',views.Detialview,name='category-view'),
    path('category-create/',views.Categorycreate,name='category-create'),
    path('createemployee/<int:pk>',views.createemployee,name='createemployee'),
    path('category-update/<int:pk>',views.Updatecategory,name='category-update'),
    path('category-delete/<int:pk>',views.deletecategory,name='category-delete'),
    path('employee-view/<int:pk>',views.Employeeview,name='employee-view'),
    path('Viewemployeeuser/<int:id>',views.Viewemployeeuser,name='Viewemployeeuser'),
    path('viewcategoryuser',views.viewcategoryuser,name='viewcategoryuser'),
    path('viewRequestadmin',views.viewRequestadmin,name='viewRequestadmin'),
    path('Sendbookingrequest/<int:id>',views.Sendbookingrequest,name='Sendbookingrequest'),
    path('Bookingrequestcreate',views.Bookingrequestcreate,name='Bookingrequestcreate'),
    path('Showallbookingrequest',views.Showallbookingrequest,name='Showallbookingrequest'),
    path('requestaccept_admin/<int:id>',views.requestaccept_admin,name='requestaccept_admin'),
    path('Viewemployeenotication',views.Viewemployeenotication,name='Viewemployeenotication'),
    path('update_workstatusemp/<int:id>/<str:uid>',views.update_workstatusemp,name='update_workstatusemp'),
    path('employeehome',views.employeehome,name='employeehome'),
    path('AdminHomePage',views.AdminHomePage,name='AdminHomePage'),
    path('userhome',views.userhome,name='userhome'),
    path('Viewworkupdation',views.Viewworkupdation,name='Viewworkupdation'),
    path('login',views.login,name='login'),
    path('LogOut',views.LogOut,name='LogOut'),
    path('View_employee_completed_work/<int:id>',views.View_employee_completed_work,name='View_employee_completed_work'),
   
    
    
    
    
    
    
  
]
