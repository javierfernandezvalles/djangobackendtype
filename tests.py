from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from DecissionsApp.models import UserProfile


class UserTestCase(TestCase):
    def setUp(self):
        joe_education = {"user_education": {"fields": [{"title": "Business and Sustainability", "place": "Tempe, AZ",
                                                        "institution_name": "Arizona State University (ASU)",
                                                        "date_finished": "Spring 2017",
                                                        "date_entered": "Fall 2015", "gpa": "5.0",
                                                        "student_email": "joe@asu.edu"}]}}
        javi_education = {"user_education": {"fields": [{"title": "Computer Science", "place": "Tempe, AZ",
                                                        "institution_name": "Arizona State University (ASU)",
                                                        "date_finished": "Fall 2018",
                                                        "date_entered": "Fall 2016", "gpa": "5.0",
                                                        "student_email": "javi@asu.edu"}]}}
        UserProfile.objects.create(first_name="Joe", last_name="DeGuzman", hometown="Philippines", current_city="Tempe",
                                   educational_background=joe_education, gender="male", marital_status="Relationship",
                                   biography="Hard Working with Bright Ideas, loves his family", verified="True")
        UserProfile.objects.create(first_name="Javi", last_name="Valles", hometown="Spain", current_city="Tempe",
                                   educational_background=javi_education, gender="male", marital_status="Single",
                                   biography="Hard Working with Bright Ideas, loves his family", verified="True")

    def test_users(self):
        """Animals that can speak are correctly identified"""
        joe = UserProfile.objects.get(first_name="Joe")
        javi = UserProfile.objects.get(first_name="Javi")
        self.assertEqual(joe.current_city, 'Tempe')
        self.assertEqual(javi.current_city, 'Tempe')
