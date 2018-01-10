from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from DecissionsApp.models import UserProfile


class UserTestCase(TestCase):
    def setUp(self):
        javi_education = {"user_education": {"fields": [{"title": "Computer Science", "place": "Tempe, AZ",
                                                        "institution_name": "Arizona State University (ASU)",
                                                        "date_finished": "Fall 2018",
                                                        "date_entered": "Fall 2016", "gpa": "5.0",
                                                        "student_email": "javi@asu.edu"}]}}
        UserProfile.objects.create(first_name="Javi", last_name="Valles", hometown="Spain", current_city="Tempe",
                                   educational_background=javi_education, gender="male", marital_status="Single",
                                   biography="Hard Working with Bright Ideas, loves his family", verified="True")

    def test_users(self):
        javi = UserProfile.objects.get(first_name="Javi")
        self.assertEqual(javi.current_city, 'Tempe')
