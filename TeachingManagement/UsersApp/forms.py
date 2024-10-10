from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Professor, Chief,CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    pass

class ProfessorRegistrationForm(forms.ModelForm):
    # Fields for the professor-specific information
    idprofessor=forms.CharField(max_length=10,required=True)
    name = forms.CharField(max_length=100, required=True, label="Name")
    family_name = forms.CharField(max_length=100, required=True, label="Family Name")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Comment")
    email = forms.EmailField(required=True, label="Email Address")

    ACTIVE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    isactive = forms.ChoiceField(choices=ACTIVE_CHOICES, required=True, label="Is active")

    class Meta:
        model = CustomUser
        fields = ['idprofessor', 'name', 'family_name', 'description', 'comment', 'email', 'isactive']
        labels = {
            'idprofessor': 'ID/DNI del Professor',
            'name': 'Nom',
            'family_name': 'Cognoms',
            'description': 'Descripció',
            'comment': 'Comentari',
            'email': 'Correu electrònic',
            'isactive': 'Està Actiu?',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        # Create or update the CustomUser
        first_name = self.cleaned_data.get('name')
        family_name = self.cleaned_data.get('family_name')
        username = f"{first_name.lower()}.{family_name.lower()}"
        generated_password = f"{first_name.lower()}_{family_name.lower()}"

        print(f"Generated password for {username}: {generated_password}")

        # Check if the user already exists
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': family_name,
                'email': self.cleaned_data.get('email'),
                'role': 'professor',
                'password': make_password(generated_password)  # Hash the password
            }
        )

        if created:
            user.set_password(generated_password)  # Set the password with the hashed value
            if commit:
                user.save()
        else:
            # Update user information if already exists
            user.first_name = first_name
            user.last_name = family_name
            user.email = self.cleaned_data.get('email')
            user.role = 'professor'
            if commit:
                user.save()

        # Save or update the associated Professor instance
        Professor.objects.update_or_create(
            idProfessor=self.cleaned_data['idprofessor'],  # Use idProfessor from the form
            defaults={
                'user': user,
                'name': first_name,
                'family_name': family_name,
                'email': self.cleaned_data.get('email'),
                'description': self.cleaned_data.get('description'),
                'comment': self.cleaned_data.get('comment'),
                'isActive': self.cleaned_data.get('isactive').lower(),  # Ensure lowercase for consistency
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

    
    def save(self, commit=True):
        # Create or update the chief instance
        chief = super().save(commit=False)

        if commit:
            chief.save()
        return chief
