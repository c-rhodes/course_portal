from functools import partial

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from course.factories import TutorFactory, CourseFactory
from course.tests.test_views import CommonTestMixin


class CourseDetailTests(APITestCase, CommonTestMixin):
    def setUp(self):
        self.url = partial(reverse, 'course-rest-api:course-detail')

    def test_get_course(self):
        tutor = TutorFactory()
        course = CourseFactory(tutors=[tutor])
        response = self.client.get(self.url(kwargs=dict(pk=course.pk)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.format_course(course, tutor))
