from django.test import TestCase
from .models import Assignment, CourseYear, Professor

# Create your tests here.
class AssignmentModelTest(TestCase):
    def test_create_valid_assignment(self):
        course_year = CourseYear.objects.create(Course="Màster en Informàtica", Year="2024-2025")
        professor = Professor.objects.create(name="Joan", family_name="Pérez", email="joan@example.com", isActive=True)
        
        assignment = Assignment.objects.create(
            CourseYear=course_year,
            Professor=professor,
            PointsA=9.5,
            PointsB=8.0,
            PointsC=7.5,
            PointsD=6.5,
            PointsE=5.0,
            PointsF=3.0,
            isCoordinator=True
        )
        
        self.assertEqual(assignment.CourseYear, course_year)
        self.assertEqual(assignment.Professor, professor)
        self.assertEqual(assignment.PointsA, 9.5)
        self.assertEqual(assignment.PointsB, 8.0)
        self.assertEqual(assignment.PointsC, 7.5)
        self.assertEqual(assignment.PointsD, 6.5)
        self.assertEqual(assignment.PointsE, 5.0)
        self.assertEqual(assignment.PointsF, 3.0)
        self.assertTrue(assignment.isCoordinator)

    def test_invalid_duplicate_assignment(self):
        course_year = CourseYear.objects.create(Course="Màster en Informàtica", Year="2024-2025")
        professor = Professor.objects.create(name="Joan", family_name="Pérez", email="joan@example.com", isActive=True)

        # Create the first assignment
        Assignment.objects.create(
            CourseYear=course_year,
            Professor=professor,
            PointsA=9.5,
            PointsB=8.0,
            PointsC=7.5,
            PointsD=6.5,
            PointsE=5.0,
            PointsF=3.0,
            isCoordinator=True
        )
        
        # Attempt to create a duplicate assignment for the same professor and course year
        with self.assertRaises(Exception):
            Assignment.objects.create(
                CourseYear=course_year,
                Professor=professor,
                PointsA=7.5,
                PointsB=6.5,
                PointsC=5.0,
                PointsD=4.5,
                PointsE=3.0,
                PointsF=1.5,
                isCoordinator=False
            )

    def test_assignment_str(self):
        course_year = CourseYear.objects.create(Course="Màster en Informàtica", Year="2024-2025")
        professor = Professor.objects.create(name="Joan", family_name="Pérez", email="joan@example.com", isActive=True)
        
        assignment = Assignment.objects.create(
            CourseYear=course_year,
            Professor=professor,
            PointsA=9.5,
            PointsB=8.0,
            PointsC=7.5,
            PointsD=6.5,
            PointsE=5.0,
            PointsF=3.0,
            isCoordinator=True
        )
        
        self.assertEqual(str(assignment), "Joan Pérez Màster en Informàtica 2024-2025")

    def test_assignment_without_points(self):
        course_year = CourseYear.objects.create(Course="Màster en Informàtica", Year="2024-2025")
        professor = Professor.objects.create(name="Joan", family_name="Pérez", email="joan@example.com", isActive=True)
        
        assignment = Assignment.objects.create(
            CourseYear=course_year,
            Professor=professor,
            PointsA=None,
            PointsB=None,
            PointsC=None,
            PointsD=None,
            PointsE=None,
            PointsF=None,
            isCoordinator=False
        )
        
        self.assertIsNone(assignment.PointsA)
        self.assertIsNone(assignment.PointsB)
        self.assertIsNone(assignment.PointsC)
        self.assertIsNone(assignment.PointsD)
        self.assertIsNone(assignment.PointsE)
        self.assertIsNone(assignment.PointsF)

    def test_assignment_with_null_points(self):
        course_year = CourseYear.objects.create(Course="Màster en Informàtica", Year="2024-2025")
        professor = Professor.objects.create(name="Joan", family_name="Pérez", email="joan@example.com", isActive=True)

        assignment = Assignment.objects.create(
            CourseYear=course_year,
            Professor=professor,
            PointsA=9.5,
            PointsB=8.0,
            PointsC=None,
            PointsD=None,
            PointsE=None,
            PointsF=None,
            isCoordinator=True
        )

        self.assertEqual(assignment.PointsA, 9.5)
        self.assertEqual(assignment.PointsB, 8.0)
        self.assertIsNone(assignment.PointsC)
        self.assertIsNone(assignment.PointsD)
        self.assertIsNone(assignment.PointsE)
        self.assertIsNone(assignment.PointsF)