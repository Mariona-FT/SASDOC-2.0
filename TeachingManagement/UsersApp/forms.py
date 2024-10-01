from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Professor, Chief,CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class CustomLoginForm(AuthenticationForm):
    # You can add custom fields here if needed
    pass

class ProfessorRegistrationForm(UserCreationForm):
    # Fields for the professor-specific information
    name = forms.CharField(max_length=100, required=True, label="Name")
    family_name = forms.CharField(max_length=100, required=True, label="Family Name")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Comment")
    email = forms.EmailField(required=True, label="Email Address")
    isactive = forms.BooleanField( required=False, label="Is active")

    class Meta:
        model = CustomUser
        # Include CustomUser fields (username, password) along with email
        fields = ['password1', 'password2', 'email']

    def save(self, commit=True):
        # Save the CustomUser first
        user = super().save(commit=False)

        #Save the USER (with role professor)
        first_name = self.cleaned_data.get('name')
        family_name = self.cleaned_data.get('family_name')

        user.username = f'{first_name}.{family_name}'.lower()  
        user.first_name = first_name
        user.last_name = family_name
        user.role = 'professor' 

        if commit:
            user.save()  # Save the CustomUser to the database
        
        professor, created = Professor.objects.get_or_create(
            user=user,
            defaults={
                'name': first_name,
                'family_name': family_name,
                'description': self.cleaned_data.get('description'),
                'comment': self.cleaned_data.get('comment'),
                'email': self.cleaned_data.get('email'),
                'isActive': self.cleaned_data.get('isactive'),
            }
        )

        # If the professor already exists, update the fields
        if not created:
            professor.name = first_name
            professor.family_name = family_name
            professor.description = self.cleaned_data.get('description')
            professor.comment = self.cleaned_data.get('comment')
            professor.email = self.cleaned_data.get('email')
            professor.isActive = self.cleaned_data.get('isactive')
            professor.save()
        return user
    

class ChiefRegistrationForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = ['professor', 'year', 'section']  # Include fields as necessary
