# services.py

from django.contrib.auth.hashers import make_password
from django.contrib import messages
import pandas as pd
from UsersApp.models import CustomUser, Professor

#REGISTER PROFESSOR MANUALLY
def register_professor_form(form, request):
    try:
        user = form.save()
        messages.success(request, f"Professor {user.first_name} {user.last_name} creat correctament.")
        print(f"User created: {user.username}, ID: {user.id}")  # Debugging line
        return user
    except Exception as e:
        print(f"Error in register_professor_form: {str(e)}")  # Debugging line
        messages.error(request, "Error al registrar el professor.")
        return None

#REGISTER PROFESSORS FILES
def process_professor_file(file, request):
    try:
        # Check file format and read content
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            messages.error(request, "Tipus de fitxer no suportat.")
            return False

        # Validate columns in the file
        required_columns = ['idProfessor', 'Name', 'FamilyName', 'Description', 'Comment', 'email', 'isActive']
        if not all(column in data.columns for column in required_columns):
            messages.error(request, f"El fitxer ha de contenir exactament les següents columnes: {', '.join(required_columns)}")
            return False

        for index, row in data.iterrows():
            try:
                username = f"{row['Name']}.{row['FamilyName']}".lower()
                password = f"{row['Name'].lower()}_{row['FamilyName'].lower()}"  # Create password

                # Check if the user already exists
                user, created = CustomUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': row['Name'],
                        'last_name': row['FamilyName'],
                        'email': row['email'],
                        'role': 'professor'
                    }
                )

                if created:
                    user.password = make_password(password)  # Hash the password
                    user.save()
                    messages.success(request, f"Professor {user.first_name} {user.last_name} creat correctament.")
                else:
                    # Update user information if already exists
                    user.first_name = row['Name']
                    user.last_name = row['FamilyName']
                    user.email = row['email']
                    user.save()
                    messages.info(request, f"Professor {user.first_name} {user.last_name} actualitzat correctament.")
                

                # Update or create Professor instance with idProfessor
                Professor.objects.update_or_create(
                    idProfessor=row['idProfessor'],  # Use idProfessor from the row
                    defaults={
                        'user': user,
                        'name': row['Name'],
                        'family_name': row['FamilyName'],
                        'email': row['email'],
                        'description': row['Description'],
                        'comment': row['Comment'],
                        'isActive': row['isActive'].lower(),
                    }
                )

            except Exception as e:
                # Handle errors specific to each row with a friendly message
                messages.warning(request, f"Error actualitzant el professor {row['Name']} {row['FamilyName']}: {str(e)}")
              
        messages.success(request, f"Professors pujats correctament.")
        return True

    except Exception as e:
        messages.error(request, f"Error de processament del fitxer: {str(e)}")
        return False
