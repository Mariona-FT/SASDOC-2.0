# SASDOC 2.0: Sistema d'Assignació de Seccions Docents

 
## Català

### Resum

Aquest projecte de fi de grau té com a objectiu desenvolupar des de zero, una plataforma en línia per optimitzar el procés d’assignació docent dins d’un departament universitari. Sorgeix com una resposta a la necessitat de trobar una solució efectiva a les limitacions del sistema actual. Actualment, aquest procés es gestiona de manera manual mitjançant fulls de càlcul i correus electrònics, una metodologia que comporta nombroses ineficiències, com ara errors en la distribució, manca de col·laboració i una despesa excessiva de temps.

La metodologia utilitzada per al desenvolupament d’aquest projecte ha sigut iterativa, amb una anàlisi prèvia del sistema actual, la identificació dels actors del sistema, els requisits funcionals i els no funcionals.

La implementació de la plataforma s’ha dut a terme amb el framework Django, per la seva facilitat d’ús, la seva estructura modular que permet possibles extensions, la gestió segura de dades i la capacitat de crear i gestionar usuaris de manera eficient. També s’han incorporat eines de disseny per garantir una interfície intuïtiva i fàcil d’utilitzar.

S’han definit tres tipus d’usuaris principals a la plataforma: director, cap de secció i professor, cadascun amb funcionalitats específiques adaptades al seu rol en el procés de gestió docent. El director té accés a la creació, modificació i eliminació de tots els paràmetres generals de la plataforma, com ara el professorat, els caps de secció, les escoles, les titulacions i les assignatures, entre altres. A més, té la responsabilitat d’introduir les dades inicials de l’assignació docent, que posteriorment, cada cap de secció assignarà al seu professorat totes les assignatures pel nou curs acadèmic. Finalment, el professorat pot accedir per veure quina és la seva assignació docent per aquell curs acadèmic.

Els resultats obtinguts han donat lloc a una plataforma que centralitza la gestió de l’assignació docent, la distribució eficient d’assignatures i la generació automàtica d’informes en formats PDF i Excel.

Aquesta eina no només minimitza de manera significativa els errors derivats dels processos manuals, sinó que també millora la transparència i fomenta una col·laboració més eficaç entre el personal docent.

Es pot confirmar que aquest projecte ha complert els objectius establerts. La plataforma no només actualitza un procés clau per al departament, sinó que també posa en evidència el potencial de la digitalització per millorar l’eficiència i la qualitat dels processos administratius.

### Paraules clau:
Assignació docent, Departament universitari, Professorat, Gestió docent, Encàrrec docent, Desenvolupament web, Plataforma en línia, Django, Html, Python

---

## Español

### Resumen

Este proyecto de fin de grado tiene como objetivo desarrollar desde cero una plataforma en línea, para optimizar el proceso de asignación docente dentro de un departamento universitario. Surge como una respuesta a la necesidad de encontrar una solución efectiva a las limitaciones del sistema actual. Actualmente, este proceso se gestiona de manera manual mediante hojas de cálculo y correos electrónicos, una metodología que presenta numerosas ineficiencias, como errores en la distribución, falta de colaboración y un consumo excesivo de tiempo.

La metodología utilizada para el desarrollo de este proyecto ha sido iterativa, incluyendo un análisis previo del sistema actual, la identificación de los actores involucrados, así como de los requisitos funcionales y no funcionales.

La implementación de la plataforma se ha realizado utilizando el framework Django, elegido por su facilidad de uso desde cero, su estructura modular que permite futuras extensiones, su gestión segura de datos y su capacidad para crear y gestionar usuarios de manera eficiente. Además, se han integrado herramientas de diseño para garantizar una interfaz intuitiva y fácil de usar.

Se han definido tres tipos principales de usuarios en la plataforma: director, jefe de sección y profesor, cada uno con funcionalidades específicas adaptadas a su rol en el proceso de gestión docente. El director tiene acceso a la creación, modificación y eliminación de todos los parámetros generales de la plataforma, como el profesorado, los jefes de sección, las escuelas, las titulaciones y las asignaturas, entre otros. Asimismo, es responsable de introducir los datos iniciales de la asignación docente que cada jefe de sección asignará posteriormente a los profesores correspondientes para todas las asignaturas del año académico. Finalmente, los profesores pueden acceder a la plataforma para consultar su asignación docente correspondiente a ese curso académico.

Los resultados obtenidos han dado lugar a una plataforma que centraliza la gestión de la asignación docente, permite la distribución eficiente de las asignaturas y genera informes automáticos en formatos PDF y Excel.

Esta herramienta no solo minimiza significativamente los errores derivados de los procesos manuales, sino que también mejora la transparencia y fomenta una colaboración más eficaz entre el personal docente.

Se puede confirmar que este proyecto ha cumplido con los objetivos establecidos. La plataforma no solo moderniza un proceso clave para el departamento, sino que también demuestra el potencial de la digitalización para mejorar la eficiencia y la calidad de los procesos administrativos.

### Palabras clave:
Asignación docente, Departamento universitario, Profesorado, Gestión docente, Encargo docente, Desarrollo web, Plataforma en línea, Django, Html, Python

---

## English

### Abstract

This final degree project aims to develop an online platform from scratch to optimize the process of teaching assignment within a university department. It arises as a response to the need to find an effective solution to the limitations of the current system. Currently, this process is managed manually using spreadsheets and emails, a methodology that presents numerous inefficiencies, such as errors in distribution, lack of collaboration, and excessive time consumption.

The methodology used for this project followed an iterative approach, including a preliminary analysis of the current system, the identification of system actors, and the definition of functional and non-functional requirements.

The platform was implemented using the Django framework, chosen for its ease of use from scratch, its modular structure that allows future extensions, its secure data management, and its ability to create and manage users efficiently. Additionally, design tools were integrated to ensure an intuitive and user-friendly interface.

Three main types of users have been defined on the platform: director, section chief, and professor, each with specific functionalities tailored to their role in the teaching management process. The director has access to the creation, modification, and deletion of all general platform parameters, such as professors, section chiefs, schools, degrees, and courses, among others. Furthermore, the director is responsible for entering the initial teaching assignment data, which each section chief will later allocate to specific professors for the corresponding courses in the academic year. Finally, professors can access the platform to view their teaching assignments for the academic year.

The results obtained have led to a platform that centralizes teaching assignment management, enables the efficient distribution of courses, and generates automatic reports in PDF and Excel formats.

This tool not only significantly reduces errors associated with manual processes but also improves transparency and fosters more effective collaboration among teaching staff.

It can be confirmed that this project has met its established objectives. The platform not only modernizes a critical process for the department but also demonstrates the potential of digitalization to enhance the efficiency and quality of administrative processes.

### Keywords:
Teaching Assignment, University Department, Faculty, Teaching Management, Teaching Task, Web Development, Online Platform, Django, HTML, Python

## Setup Instructions
Follow these steps to set up and run the SASDOC 2.0 project locally:

#### 1. Clone the repository:
```
git clone https://github.com/Mariona-FT/SASDOC-2.0.git
cd SASDOC-2.0
```
#### 2.  Create a Virtual Environment:
In the project directory (SASDOC-2.0), create a virtual environment to isolate dependencies:

```
python -m venv venv
```
#### 3. Activate the Virtual Environment:
Activate the virtual environment using the following command:

- For Windows:
```
.\venv\Scripts\activate
```
- Linux/Mac:
```
source venv/bin/activate
```
Your environment structure should look like this:

```
\SASDOC-2.0
├── TeachingManagement
├──  venv
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```

#### 4. Install Dependencies:
Navigate to the `TeachingManagement` directory and install the required dependencies:

```
cd .\TeachingManagement\
pip install -r requirements.txt
```
#### 5. Apply Migrations:
Run the following commands to set up the database and apply migrations:

```
python manage.py makemigrations
```
If doesnt work, try to make migrations for each app with **this order**:
```
 python manage.py makemigrations UsersApp
 python manage.py makemigrations AcademicInfoApp
 python manage.py makemigrations ProfSectionCapacityApp
 python manage.py makemigrations AssignmentYearApp
```
You should see something like this for each migration:
```  
Migrations for 'AcademicInfoApp':
  AcademicInfoApp\migrations\0001_initial.py
    + Create model Field
    + Create model Language
    + Create model School
    + Create model Section
    + Create model TypeProfessor
    + Create model Year
    + Create model Degree
    + Add field Section to school
    + Create model Course
Migrations for 'ProfSectionCapacityApp':
  ProfSectionCapacityApp\migrations\0001_initial.py
    + Create model Capacity
    + Create model CapacitySection
    + Create model CourseYear
    + Create model Free
    + Create model TypePoints
  ProfSectionCapacityApp\migrations\0002_initial.py
    + Add field Professor to capacity
    + Add field Year to capacity
    + Add field Professor to capacitysection
    + Add field Section to capacitysection
    + Add field Year to capacitysection
    + Add field Course to courseyear
    + Add field Language to courseyear
    + Add field Year to courseyear
    + Add field Professor to free
    + Add field Year to free
    + Add field Section to typepoints
    + Add field Year to typepoints
    ~ Alter unique_together for capacity (1 constraint(s))
    ~ Alter unique_together for capacitysection (1 constraint(s))
    ~ Alter unique_together for courseyear (1 constraint(s))
    ~ Alter unique_together for typepoints (1 constraint(s))
Migrations for 'UsersApp':
  UsersApp\migrations\0001_initial.py
    + Create model Professor
    + Create model Chief
    + Create model ProfessorField
    + Create model ProfessorLanguage
    + Create model CustomUser
    + Add field user to professor
```
Finally, apply all migrations:
```
python manage.py migrate
```
You should see confirmation of successful migrations like:
```
Operations to perform:
  Apply all migrations: AcademicInfoApp, ProfSectionCapacityApp, UsersApp, admin, auth, contenttypes, sessions
Running migrations:
  Applying AcademicInfoApp.0001_initial... OK
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying UsersApp.0001_initial... OK
  Applying ProfSectionCapacityApp.0001_initial... OK
  Applying ProfSectionCapacityApp.0002_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying sessions.0001_initial... OK

```
#### 6. Create a Superuser:
Create a superuser to access the Django admin panel:

```
python manage.py createsuperuser
```

> Enter the username (e.g., admin).

> Enter the email address (e.g., a@gmail.com).

> Enter the password (make sure it meets the security requirements).

> Note: If the password is too common or short, you can bypass the validation by typing y when prompted.


#### 7. Run the Development Server:
Start the Django development server by running:

```
python manage.py runserver
```
The development server will start at http://127.0.0.1:8000/.

#### 8. Access the Admin Panel:
To access the Django admin panel, visit: http://127.0.0.1:8000/admin

Login with the superuser credentials you created earlier (admin and the password).

#### 9. Create a Director User:
Once logged in to the admin panel, create a new user with the role of **director**.

#### 10. Access the Application: 
After creating the director user, log out of the admin panel, and log in again using the newly created director credentials at: http://127.0.0.1:8000/baseapp/




Now you're ready to use the <ins> **SASDOC 2.0 platform**</ins>! Enjoy exploring the features and testing the system. If you encounter any issues, have suggestions, or need help, feel free to open an issue in the repository. I welcome contributions and feedback!🌟
