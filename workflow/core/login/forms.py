from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Rol
from django import forms


  

class RegisterForm(UserCreationForm):
 
    class Meta:
        model = Usuario
        fields = ["rol", "empresa", "unidad", "cargo", "rut", "nombres", "apellidos" , "telefono", "direccion","correo", "password1", "password2", ]
        widgets={  
        
            'rol': forms.Select(attrs={'class':'form-control', 'onchange' : 'Cambiar()'} ), 
            'empresa': forms.Select(attrs={'class':'form-control', 'onchange' : 'cambiarUnidad()', 'required': 'True' }),
            'rut' :  forms.TextInput(attrs={'placeholder': 'Ingresar Rut', 'oninput' : 'checkRut(this)'}),
            'nombres' :  forms.TextInput(attrs={'placeholder': 'Ingresar Nombres'}),
            'apellidos' :  forms.TextInput(attrs={'placeholder': 'Ingresar Apellidos'}),
            'telefono' :  forms.TextInput(attrs={'placeholder': 'Ingresar Telefono', 'type': 'number'}),
            'direccion' :  forms.TextInput(attrs={'placeholder': 'Ingresar Direccion'}),
            'correo' :  forms.TextInput(attrs={'placeholder': 'Ingresar Correo Electronico'}),
            'password1' :  forms.PasswordInput(attrs={'placeholder': 'Ingresar Contraseña'}),
            'password2' :  forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
            
            
             
        }


    
    
    
  
   