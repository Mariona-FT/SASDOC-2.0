from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Professor, Chief,CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    pass

class ProfessorRegistrationForm(forms.ModelForm):
    # Fields for the professor-specific information
    idprofessor = forms.CharField(max_length=10, required=True, label="ID/DNI del Professor")
    name = forms.CharField(max_length=100, required=True, label="Nom")
    family_name = forms.CharField(max_length=100, required=True, label="Cognoms")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Descripció")
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Comentari")
    email = forms.EmailField(required=True, label="Correu electrònic")

    ACTIVE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    isactive = forms.ChoiceField(choices=ACTIVE_CHOICES, required=True, label="Està Actiu?")

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = {
            'username': 'Nom del usuari',
            'email': 'Correu electrònic',
        }

    def clean(self):
        cleaned_data = super().clean()
        idprofessor = cleaned_data.get('idprofessor')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # Check if a user with the same username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(f'El nom d\'usuari "{username}" ja està en ús.')

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(f'El correu electrònic "{email}" ja està en ús.')

        # Check if a professor with the same ID already exists
        if Professor.objects.filter(idProfessor=idprofessor).exists():
            raise ValidationError(f'El ID del professor "{idprofessor}" ja està en ús.')

        return cleaned_data
    def save(self, commit=True):
        # Get the CustomUser instance from the form
        user = self.instance

        # Update the fields from the form
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('family_name')
        user.email = self.cleaned_data.get('email')
        generated_password = f"{user.first_name.lower()}_{user.last_name.lower()}"
        user.password= make_password(generated_password)  # Hash the password

        if commit:
            user.save()  # Save the user instance

        # Also update the associated Professor instance
        Professor.objects.update_or_create(
            user=user,  # Link to the same CustomUser
            defaults={
                'idProfessor': self.cleaned_data['idprofessor'],
                'name': self.cleaned_data['name'],
                'family_name': self.cleaned_data['family_name'],
                'email': self.cleaned_data['email'],
                'description': self.cleaned_data['description'],
                'comment': self.cleaned_data['comment'],
                'isActive': self.cleaned_data['isactive'].lower(),
            }
        )

        return user
    
#To upload files .csv 
class UploadFileForm(forms.Form):
    file = forms.FileField(label="Puja un fitxer de tipus CSV o Excel:")


class ChiefRegistrationForm(forms.ModelForm):
   
    class Meta:
        model = Chief
        fields = ['professor', 'year', 'section'] 
        labels = {
            'professor': 'Nom del Professor',
            'year': 'Any',
            'section':'Secció',
        }

    def save(self, commit=True):
        # Create or update the chief instance
        chief = super().save(commit=False)

        if commit:
            chief.save()
        return chief
