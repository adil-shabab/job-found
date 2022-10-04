from unicodedata import category
from django.shortcuts import render,redirect
from api.forms import LoginForm,CategoryForm
from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from .serializers import   BookingreqSerializers, CategorySerializers, EmployeeSerializers,FileSerializer,UserregSerializers,SelectedEmployeeSerializers,UpdateEmployeeSerializers
from.models import  Bookingreq, Category, Employee, Login, Userregister, workupdate,File
from api import serializers
from django.db import connection
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.http.response import JsonResponse


def index(request):
    return render(request, 'index.html')
      
def AdminHomePage(request):
    return render(request,"admin/PageHeader.html")
   
def employeehome(request):
    return render(request,"employee/employeehome.html")
def userhome(request):
    return render(request,"user/pageheader.html")

def LogOut(request):
    return render(request, 'LogOut.html')
@api_view(['POST'])
def login(request):   
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form['user_id'].value()
            password = form['password'].value()

            try:
                user = Login.objects.get(user_id=user_id, password=password)
                if user is not None:
                    return redirect("../AdminHomePage")
            except:
                pass
            try:
                user = Userregister.objects.get(user_id=user_id, password=password)
                if user is not None:

                    request.session['uid'] = user.id
                    print(user.id)
                    return redirect("../userhome")
            except:
                pass
            
            
            try:
                user = Employee.objects.get(user_id=user_id, password=password)
                if user is not None:
                    request.session['eid'] = user.id
                    print(user.id)
                    return redirect("../employeehome")
            
            except:
                pass    


    form = LoginForm()
    return render(request, 'login.html', {'form': form})

@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'list':'/job-category/',
        'detial view':'/job-detials/<int:id>',
        'create':'/category-create/',
        'update':'/category-update/<int:id>',
        'delete':'/category-delete/<int:id>',
    }
    return Response(api_urls);

@api_view(['GET'])
def Showall(request):
    category=Category.objects.all()
    serializer=CategorySerializers(category, many=True)
    return JsonResponse({"categories": serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def Detialview(request,pk):
    category=Category.objects.get(id=pk)
    serializer=CategorySerializers(category, many=False)
    return JsonResponse({"categories": serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
def Categorycreate(request):
    serializer=CategorySerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data['response'] = ' Category Added'
    
    else:
        data = serializer.errors
        
    return Response(data, status=status.HTTP_200_OK)   

@api_view(['POST'])
def Updatecategory(request,pk):
    category=Category.objects.get(id=pk)
    serializer=CategorySerializers(instance=category,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def deletecategory(request,pk):
    category=Category.objects.get(id=pk)
    category.delete()
    return Response('item deleted sucessfully')

@api_view(['POST'])
def Employeecreate(request,pk):
    category=Category.objects.get(id=pk)
    serializer=EmployeeSerializers(instance=category,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def Sendbookingrequest(request,id):
    employee=Employee.objects.get(id=id)
    serializer=BookingreqSerializers(instance=employee,data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data['response'] = 'Booked'
    else:
        data = serializer.errors
        
    return Response(data, status=status.HTTP_200_OK)   

@api_view(['GET'])
def Employeeview(request,pk):
    employee=Employee.objects.filter(category=pk)
    serializer=EmployeeSerializers(employee,many=True)
    return JsonResponse({"Employees": serializer.data}, safe=False, status=status.HTTP_200_OK)

def viewRequestadmin(request):
    cat=Bookingreq.objects.all()
    print(cat)
    return render(request, "admin/viewRequestadmin.html", {'cat': cat})

def requestaccept_admin(request,id):
    data=Bookingreq.objects.get(id=id)
    data.status='accepted'
    data.save()
    return redirect("../viewRequestadmin")

#---------------------------------user------------------------------------------------------------------#

def viewcategoryuser(request):
    cat=Category.objects.all()
    return render(request, "viewcategoryuser.html", {'cat': cat})

def Viewemployeeuser(request,id):
    cat=Employee.objects.filter(category=id)
    
    return render(request,"Viewemployeeuser.html",{'cat':cat})

def Viewworkupdation(request):
    uid=request.session['uid']
    print(uid,"hi")
    cat=workupdate.objects.filter(id=uid,status='COMPLETED')
    print(cat)
    return render(request,"user/Viewworkupdation.html",{'cat':cat})

#---------------------------------------------------employee----------------#

def Viewemployeenotication(request):
    eid=request.session['eid']
    cat=Bookingreq.objects.filter(employee=eid,status='accepted')
    print(cat)
    return render(request,"employee/Viewemployeenotication.html",{'cat':cat})

def update_workstatusemp(request,id,uid):
    status = 'COMPLETED'
    user_id = uid
    bookingreq = Bookingreq.objects.get(id=id)
    data = workupdate(user_id=user_id,bookingreq=bookingreq,status=status)
    data.save()
    return redirect("/employeehome")

def View_employee_completed_work(request,id):
    cat=workupdate.objects.filter(bookingreq=id,status='COMPLETED')
    print(cat)
    return render(request,"employee/View_employee_completed_work.html",{'cat':cat})



@api_view(['GET'])
def SelectEmployee(request,pk):
    employee=Employee.objects.get(id=pk)
    serializer=SelectedEmployeeSerializers(employee,many=False)
    return JsonResponse({"Selected Employee": serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
def Bookingrequestcreate(request):
    serializer=BookingreqSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data['response'] = 'Booked'
    else:
        data = serializer.errors
        
    return Response(data, status=status.HTTP_200_OK)   

@api_view(['GET'])
def Showallbookingrequest(request):
    bookings=Bookingreq.objects.all()
    serializer=BookingreqSerializers(bookings, many=True)
    return Response(serializer.data)

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    
    def post(self, request, *args, **kwargs):
      
      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Showallemployee(request):
    file=Employee.objects.all()
    serializer=EmployeeSerializers(file, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createemployee(request,pk):
    data = request.data
    category=Category.objects.get(id=pk)
    note = Employee.objects.create(
        user_id=data['user_id'],
        lastname=data['lastname'],
        category=category,
        description=data['description'],
        Adhaar_no=data['Adhaar_no'],
        adhaar_img=data['adhaar_img'],
        address=data['address'],
        password=data['password'],
        phone=data['phone'],
        state=data['state'],
        district=data['district'],
        pincode=data['pincode'],                
    )
    serializer = EmployeeSerializers(note,many=False)
    return Response(serializer.data) 



@api_view(['POST'])
def Updateregistration(request,id):
    employee=Employee.objects.get(id=id)
    serializer=EmployeeSerializers(instance=employee,data=request.data,many=False)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data['response'] = 'check box selected'
    else:
        data = serializer.errors
        
    return Response(data, status=status.HTTP_200_OK)
  

def login(request):   
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form['user_id'].value()
            password = form['password'].value()

            try:
                user = Login.objects.get(user_id=user_id, password=password)
                if user is not None:
                    return redirect("../AdminHomePage")
            except:
                pass
            try:
                user = Userregister.objects.get(user_id=user_id, password=password)
                serializer=UserregSerializers(instance=user,data=request.data)
                if user is not None:

                    request.session['uid'] = user.id
                    print(user.id)
                    return redirect("../userhome")
            except:
                pass
            
            
            try:
                user = Employee.objects.get(user_id=user_id, password=password)
                if user is not None:
                    request.session['eid'] = user.id
                    print(user.id)
                    return redirect("../employeehome")
            
            except:
                pass    


    form = LoginForm()
    return render(request, 'login.html', {'form': form})

@api_view(['POST'])
def login_api(request):
    data = request.data
    user_id=data['user_id']
    password=data['password']
    try:
        note=Userregister.objects.get(user_id=user_id,password=password)
        serializer = UserregSerializers(note,many=False)
        if note is not None:
            return Response(serializer.data)
              
    except:
        pass  
      
    try:

        note=Employee.objects.get(user_id=user_id,password=password)
        serializer = EmployeeSerializers(note,many=False)
        return Response(serializer.data)
    except:
        pass  
    
    
#--------------------------------adminhomepage---------------------------------------------#

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/add_category')
            except:
                pass
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})


def view_category(request):
    cat = Category.objects.all()
    print("data:")
    return render(request, "admin/view_category.html", {'cat': cat})


def edit_category(request,id):
    cat=Category.objects.get(id=id)
    return render(request,"admin/edit_category.html",{'cat':cat})


def update_category(request, id):
    cat = Category.objects.get(id=id)
    print(id)
    form = CategoryForm(request.POST,instance=cat)
    if form.is_valid():
        form.save()
        return redirect("../view_category")
    return render(request, 'edit_category.html', {'cat': cat}) 
  
