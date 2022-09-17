from unicodedata import category
from django.db import models




class Login(models.Model):
    user_id=models.CharField(max_length=40)
    password=models.CharField(max_length=40)

    def _str_(self):
        return self.user_id
    


class Category(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)

    def _str_(self):
        return self.name
    
    
    
    

class Userregister(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)
    lastname=models.CharField(max_length=200, null=False, blank=False)
    email=models.CharField(max_length=200, null=False, blank=False)
    phone=models.CharField(max_length=200, null=False, blank=False)
    password=models.CharField(max_length=200, null=False, blank=False)

    def _str_(self):
        return self.name    
    
    
    
    
class Employee(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)
    lastname=models.CharField(max_length=200, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(max_length=200, null=False, blank=False)
    Adhaar_no=models.IntegerField(null=True, blank=True)
    adhaar_img=models.ImageField(upload_to='adhaarimg',null=True, blank=True)
    password=models.TextField(max_length=200,null=True, blank=True)
    

    def _str_(self):
        return self.name
    
    
    
    
    
class Bookingreq(models.Model):
    userregister=models.ForeignKey(Userregister,on_delete=models.CASCADE,null=True, blank=True)
    description=models.TextField(max_length=200, null=False, blank=False)
    date=models.DateField(null=True, blank=True)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    status=models.CharField(max_length=200, null=True, blank=True)
    

    def _str_(self):
        return self.username    
    
    
class workupdate(models.Model):
    user_id=models.CharField(max_length=200, null=True, blank=True)
    bookingreq=models.ForeignKey(Bookingreq,on_delete=models.CASCADE)
    status=models.CharField(max_length=200, null=True, blank=True)
   

    def _str_(self):
        return self.user_id     
    
    
    
    

class File(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)
    lastname=models.CharField(max_length=200, null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(max_length=200, null=False, blank=False)
    Adhaar_no=models.IntegerField(null=True, blank=True)
    password=models.TextField(max_length=200,null=True, blank=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
 
    
    
    
      
       


