# services.py

from django.contrib.auth.hashers import make_password
from django.contrib import messages
import pandas as pd
from UsersApp.models import CustomUser, Professor

def register_professor_form(form, request):
    user=form.save() 
    messages.success(request,f"Professor {user.first_name} {user.last_name} creat correctament.")
    return user


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
        required_columns = ['nom', 'cognom', 'email', 'descripcio', 'comentaris', 'esactiu']
        if not all(column in data.columns for column in required_columns):
            messages.error(request, f"El fitxer ha de contenir exactament les següents columnes: {', '.join(required_columns)}")
            return False

        # Loop through the data and update/create professors
        for index, row in data.iterrows():
            try:
                username = f"{row['nom']}.{row['cognom']}".lower()
                password = f"{row['nom'].lower()}_{row['cognom'].lower()}"  # Create password

                # Check if the user already exists
                user, created = CustomUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': row['nom'],
                        'last_name': row['cognom'],
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
                    user.first_name = row['nom']
                    user.last_name = row['cognom']
                    user.email = row['email']
                    user.save()
                    messages.info(request, f"Professor {user.first_name} {user.last_name} actualitzat correctament.")

                # Update or create Professor instance
                Professor.objects.update_or_create(
                    user=user,
                    defaults={
                        'name': row['nom'],
                        'family_name': row['cognom'],
                        'email': row['email'],
                        'description': row['descripcio'],
                        'comment': row['comentaris'],
                        'isActive': row['esactiu']
                    }
                )

            except Exception as e:
                # Handle errors specific to each row with a friendly message
                messages.warning(request, f"Error actualitzant el professor {row['nom']} {row['cognom']}.")
        
        messages.success(request, f"Professors pujats correctament.")
        return True

    except Exception as e:
        messages.error(request, f"Error de processament del fitxer: {str(e)}")
        return False
