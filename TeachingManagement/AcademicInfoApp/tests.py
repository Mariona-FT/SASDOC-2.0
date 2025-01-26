from django.test import TestCase

# Create your tests here.
from AcademicInfoApp.models import Field, Section, School, Degree, Course, TypeProfessor, Language, Year
from AcademicInfoApp.forms import FieldForm, SectionForm, SchoolForm, DegreeForm, CourseForm, TypeProfessorForm, LanguageForm, YearForm

class FieldModelTest(TestCase):
    def test_field_creation(self):
        field = Field.objects.create(NameField="Enginyeria", Description="Camp Tècnic", isActive=True)
        self.assertEqual(field.NameField, "Enginyeria")
        self.assertTrue(field.isActive)

class SectionModelTest(TestCase):
    def test_section_creation(self):
        section = Section.objects.create(NameSection="Vilanova", LetterSection="V", isActive=True)
        self.assertEqual(section.NameSection, "Vilanova")
        self.assertEqual(section.LetterSection, "V")

class SchoolModelTest(TestCase):
    def test_school_creation(self):
        section = Section.objects.create(NameSection="Manresa", LetterSection="M")
        school = School.objects.create(NameSchool="EPSEVG", CodeSchool=1234, Section=section)
        self.assertEqual(school.NameSchool, "EPSEVG")
        self.assertEqual(school.CodeSchool, 1234)
        self.assertEqual(school.Section, section)

class DegreeModelTest(TestCase):
    def test_degree_creation(self):
        section = Section.objects.create(NameSection="TIC", LetterSection="T")
        school = School.objects.create(NameSchool="Universitat", CodeSchool=5678, Section=section)
        degree = Degree.objects.create(NameDegree="Informàtica", CodeDegree=101, School=school)
        self.assertEqual(degree.NameDegree, "Informàtica")
        self.assertEqual(degree.School, school)

class CourseModelTest(TestCase):
    def test_course_creation(self):
        field = Field.objects.create(NameField="Matemàtiques")
        section = Section.objects.create(NameSection="Campus Nord", LetterSection="NOD")
        school = School.objects.create(NameSchool="ETSEIIAT", CodeSchool=91011, Section=section)
        degree = Degree.objects.create(NameDegree="Física", CodeDegree=202, School=school)
        course = Course.objects.create(NameCourse="Mecànica Quàntica", CodeCourse=303, ECTS=5.0, Degree=degree, Field=field)
        self.assertEqual(course.NameCourse, "Mecànica Quàntica")
        self.assertEqual(course.Degree, degree)
        self.assertEqual(course.Field, field)

class TypeProfessorModelTest(TestCase):
    def test_type_professor_creation(self):
        type_professor = TypeProfessor.objects.create(NameContract="Associat 2", isFullTime=True, isPermanent=True)
        self.assertEqual(type_professor.NameContract, "Associat 2")
        self.assertTrue(type_professor.isFullTime)
        self.assertTrue(type_professor.isPermanent)

class LanguageModelTest(TestCase):
    def test_language_creation(self):
        language = Language.objects.create(Language="Anglès")
        self.assertEqual(language.Language, "Anglès")

class YearModelTest(TestCase):
    def test_year_creation(self):
        year = Year.objects.create(Year="2024-2025", isEditable=True)
        self.assertEqual(year.Year, "2024-2025")
        self.assertTrue(year.isEditable)

## FORMS
class FieldFormTest(TestCase):
    def test_valid_field_form(self):
        form_data = {'NameField': 'Ciències', 'Description': 'Àrea d\'estudi', 'isActive': True}
        form = FieldForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_field_form(self):
        form_data = {'NameField': '', 'Description': 'Àrea d\'estudi', 'isActive': True}
        form = FieldForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameField', form.errors)

class SectionFormTest(TestCase):
    def test_valid_section_form(self):
        form_data = {'NameSection': 'Secció A', 'LetterSection': 'A', 'isActive': True}
        form = SectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_section_form(self):
        form_data = {'NameSection': '', 'LetterSection': 'A', 'isActive': True}
        form = SectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameSection', form.errors)

class SchoolFormTest(TestCase):
    def test_valid_school_form(self):
        section = Section.objects.create(NameSection="Secció A", LetterSection="A", isActive=True)
        form_data = {'NameSchool': 'Institut', 'CodeSchool': 1234, 'Section': section.idSection, 'isActive': True}
        form = SchoolForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_school_form(self):
        form_data = {'NameSchool': '', 'CodeSchool': 1234, 'Section': 1, 'isActive': True}
        form = SchoolForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameSchool', form.errors)

class DegreeFormTest(TestCase):
    def test_valid_degree_form(self):
        section = Section.objects.create(NameSection="Secció A", LetterSection="A", isActive=True)
        school = School.objects.create(NameSchool="Universitat", CodeSchool=1234, Section=section)
        form_data = {'NameDegree': 'Informàtica', 'CodeDegree': 101, 'School': school.idSchool, 'isActive': True}
        form = DegreeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_degree_form(self):
        section = Section.objects.create(NameSection="Secció A", LetterSection="A", isActive=True)
        school = School.objects.create(NameSchool="Universitat", CodeSchool=1234, Section=section)
        form_data = {'NameDegree': '', 'CodeDegree': 101, 'School': school.idSchool, 'isActive': True}
        form = DegreeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameDegree', form.errors)

class CourseFormTest(TestCase):
    def test_valid_course_form(self):
        field = Field.objects.create(NameField="Ciències")
        section = Section.objects.create(NameSection="Secció A", LetterSection="A", isActive=True)
        school = School.objects.create(NameSchool="Col·legi", CodeSchool=1234, Section=section)
        degree = Degree.objects.create(NameDegree="Informàtica", CodeDegree=101, School=school)
        form_data = {'NameCourse': 'Introducció a la Informàtica', 'CodeCourse': 101, 'ECTS': 5, 'Degree': degree.idDegree, 'Field': field.idField, 'isActive': True}
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_course_form(self):
        form_data = {'NameCourse': '', 'CodeCourse': 101, 'ECTS': 5, 'Degree': 1, 'Field': 1, 'isActive': True}
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameCourse', form.errors)

class TypeProfessorFormTest(TestCase):
    def test_valid_type_professor_form(self):
        form_data = {'NameContract': 'Temps complet', 'isFullTime': True, 'isPermanent': True, 'Comment': 'Professor de temps complet', 'isActive': True}
        form = TypeProfessorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_type_professor_form(self):
        form_data = {'NameContract': '', 'isFullTime': True, 'isPermanent': True, 'Comment': 'Professor de temps complet', 'isActive': True}
        form = TypeProfessorForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('NameContract', form.errors)

class LanguageFormTest(TestCase):
    def test_valid_language_form(self):
        form_data = {'Language': 'Anglès'}
        form = LanguageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_language_form(self):
        form_data = {'Language': ''}
        form = LanguageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Language', form.errors)

class YearFormTest(TestCase):
    def test_valid_year_form(self):
        form_data = {'Year': '2024-2025', 'isEditable': True}
        form = YearForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_form(self):
        form_data = {'Year': '', 'isEditable': True}
        form = YearForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Year', form.errors)