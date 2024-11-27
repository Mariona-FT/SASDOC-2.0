from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Professor, Chief,CustomUser,ProfessorField,ProfessorLanguage
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from AcademicInfoApp.models import Field,Language,TypeProfessor,Year



User = get_user_model()

class CustomLoginForm(AuthenticationForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #username field
        self.fields['username'].widget = forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Nom d\'usuari (username)','autofocus': True,})
        self.fields['username'].label = 'Usuari'

        # password field
        self.fields['password'].widget = forms.PasswordInput( attrs={'class': 'form-control',  'placeholder': 'Contrasenya', })
        self.fields['password'].label = 'Contrasenya'

#Final Form for Professor
class ProfessorForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nom d'usuari", 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Sisplau, entreu un nom d'usuari únic."
    ) 
    
    # idprofessor = forms.CharField(
    #     max_length=10, 
    #     required=True, 
    #     label="ID/DNI del Professor", 
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    # )  

    name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nom", 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    ) 

    family_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Cognoms", 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )  

    description = forms.CharField(
        required=False, 
        label="Descripció", 
        widget=forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
        help_text="Per si es vol una breu descripció del professor des de equip Directiu."
    ) 

    comment = forms.CharField(
        required=False, 
        label="Comentari", 
        widget=forms.Textarea(attrs={'rows': 3,'class': 'form-control'}),
        help_text=" Per si es vol afegir un comentari des del Cap de Secció."
    ) 

    email = forms.EmailField(
        required=True, 
        label="Correu electrònic", 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    ACTIVE_CHOICES = [
        ('yes', 'Si'),
        ('no', 'No'),
    ]

    isactive = forms.ChoiceField(
        choices=ACTIVE_CHOICES, 
        required=True, 
        label="Està Actiu?", 
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Seleccioneu si el professor està Actiu."
    )   

    current_contract = forms.ModelChoiceField(
        queryset=TypeProfessor.objects.all(),
        required=True,
        label="Assignar Contracte vigent",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    possible_fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.filter(isActive=True),
        required=False,
        label="Assignar Camps d'estudi",
        widget=forms.CheckboxSelectMultiple,

    )
    possible_languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False,
        label="Assignar Idiomes",
        widget=forms.CheckboxSelectMultiple, 
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = {
            'username': 'Nom del usuari',
            'email': 'Correu electrònic',
        }
    
    def __init__(self, *args,professor=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Set initial values for professor fields and languages
        if professor:
            self.fields['username'].initial = professor.user.username 
            self.fields['name'].initial = professor.name
            self.fields['family_name'].initial = professor.family_name
            self.fields['description'].initial = professor.description
            self.fields['comment'].initial = professor.comment
            self.fields['email'].initial = professor.email
            self.fields['isactive'].initial = 'yes' if professor.isActive == 'yes' else 'no'
           
            self.fields['current_contract'].initial = professor.current_contract 
            self.fields['possible_fields'].initial = professor.professor_fields.values_list('Field', flat=True)
            self.fields['possible_languages'].initial = professor.professor_languages.values_list('Language', flat=True)
        

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        print("Cleaned data before validation:", cleaned_data)  # Print cleaned data before checks

        # Get the current instance to exclude it from the uniqueness check
        user_instance = self.instance

        if CustomUser.objects.filter(username=username).exclude(pk=user_instance.pk).exists():
            raise ValidationError(f'El nom d\'usuari "{username}" ja està en ús.')

        # Check if a user with the same email already exists, excluding the current user
        if CustomUser.objects.filter(email=email).exclude(pk=user_instance.pk).exists():
            raise ValidationError(f'El correu electrònic "{email}" ja està en ús.')

        print("Cleaned data after validation:", cleaned_data)  # Print cleaned data after checks
        return cleaned_data
    
    def save(self, commit=True):
       
        user = self.instance or CustomUser()
        professor = getattr(user, 'professor', None)

        current_contract = self.cleaned_data['current_contract']
        
        # Update user fields
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['family_name']
       
        if commit:
            user.save()
        
        if not user.pk:  # Only set password for new user
            generated_password = f"{user.first_name.lower()}_{user.last_name.lower()}"
            user.password = make_password(generated_password)
        
        print("User data before saving:", user)  # Print user instance before saving

        if commit:
            user.save()
        
        # Update or create professor instance
        professor, created = Professor.objects.update_or_create(
            user=user,
            defaults={
                'name': self.cleaned_data['name'],
                'family_name': self.cleaned_data['family_name'],
                'email': self.cleaned_data['email'],
                'description': self.cleaned_data['description'],
                'comment': self.cleaned_data['comment'],
                'isActive': self.cleaned_data['isactive'].lower(),
                'current_contract':self.cleaned_data['current_contract'],
            }
        )
        print("Professor data saved:", professor)  # Print professor instance after saving

        if commit:
            professor.save()

            possible_fields = self.cleaned_data['possible_fields']
            possible_languages = self.cleaned_data['possible_languages']
                
            professor.professor_fields.all().delete()  # Clear existing fields
            for field in possible_fields:
                professor.professor_fields.create(Field=field)

            professor.professor_languages.all().delete()  # Clear existing languages
            for language in possible_languages:
                professor.professor_languages.create(Language=language)
                
        return user

#Basic form for professor - Not USED
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

        # Get the current instance to exclude it from the uniqueness check
        user_instance = self.instance

        # Check if a user with the same username already exists, excluding the current user
        if CustomUser.objects.filter(username=username).exclude(pk=user_instance.pk).exists():
            raise ValidationError(f'El nom d\'usuari "{username}" ja està en ús.')

        # Check if a user with the same email already exists, excluding the current user
        if CustomUser.objects.filter(email=email).exclude(pk=user_instance.pk).exists():
            raise ValidationError(f'El correu electrònic "{email}" ja està en ús.')

        # Check if a professor with the same ID already exists, excluding the current professor
        if Professor.objects.filter(idProfessor=idprofessor).exclude(user=user_instance).exists():
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

#Form to enter extra info in professor - NOT USED  
class ExtraInfoProfessor(forms.ModelForm):
    # Multiple choice fields for related models (fields and languages)
    possible_fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.filter(isActive=True),  # Assuming isActive indicates available fields
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assignar Camps d'estudi"
    )
    possible_languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assignar Idiomes"
    )

    # Single choice field for the current contract (TypeProfessor)
    current_contract = forms.ModelChoiceField(
        queryset=TypeProfessor.objects.all(),
        required=True,  # Since it should be a single contract, it's mandatory
        label="Assignar Contracte vigent"
    )

    class Meta:
        model = Professor
        fields = ['current_contract']  

    def __init__(self, *args, **kwargs):
        professor = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Set initial values for professor fields and languages
        if professor:
            self.fields['possible_fields'].initial = professor.professor_fields.values_list('Field', flat=True)
            self.fields['possible_languages'].initial = professor.professor_languages.values_list('Language', flat=True)

    def save(self, commit=True):
        professor = super().save(commit=False)
        possible_fields = self.cleaned_data['possible_fields']
        possible_languages = self.cleaned_data['possible_languages']

        if commit:
            professor.save()

            # Save the many-to-many relations
            ProfessorField.objects.filter(Professor=professor).delete()  # Clear existing entries
            for field in possible_fields:
                ProfessorField.objects.create(Professor=professor, Field=field)

            ProfessorLanguage.objects.filter(Professor=professor).delete()  # Clear existing entries
            for language in possible_languages:
                ProfessorLanguage.objects.create(Professor=professor, Language=language)

        return professor

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

        widgets = {
            'professor': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'year': forms.Select(attrs={'required': 'required','class': 'form-select'}),
            'section': forms.Select(attrs={'required': 'required','class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['professor'].queryset = Professor.objects.all().order_by('family_name')
        self.fields['year'].queryset = Year.objects.all().order_by('-Year')

    def clean(self):
        cleaned_data = super().clean()
        professor = cleaned_data.get('professor')
        year = cleaned_data.get('year')
        section = cleaned_data.get('section')
        
        # Check if we are editing an existing Chief (i.e., it has a pk)
        instance = self.instance  # The current instance of Chief being edited

        if instance.pk:
            # Exclude the current instance from the query to allow for editing the same object
            if Chief.objects.filter(professor=professor, year=year, section=section).exclude(pk=instance.pk).exists():
                raise ValidationError('Aquest Professor, amb aquest Any i Secció ja existeix.')

        else:
            # Check if a Chief already exists with the same professor, year, and section (for new entries)
            if Chief.objects.filter(professor=professor, year=year, section=section).exists():
                raise ValidationError('Aquest Professor, amb aquest Any i Secció ja existeix.')

        return cleaned_data
    
    def save(self, commit=True):
        # Create or update the chief instance
        chief = super().save(commit=False)
        
        # Check if we are updating an existing chief
        if chief.pk:  # If the chief already exists
            old_professor = Chief.objects.get(pk=chief.pk).professor
            # Check if the professor being changed
            if chief.professor != old_professor:
                # Revert old professor's role if they have no other chiefs
                if old_professor.chief_set.count() == 1:
                    old_professor.user.role = 'professor'
                    old_professor.user.save()
        
        # Set the new role for the new professor
        chief.professor.user.role = 'section_chief'

        if commit:
            # Save the professor's role and the chief instance
            chief.professor.user.save()  
            chief.save() 
             
        return chief
