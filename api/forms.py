from django import forms
from . models import Login,Category



class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = "__all__"
        widgets = {
        }
        
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
        }
        
        
