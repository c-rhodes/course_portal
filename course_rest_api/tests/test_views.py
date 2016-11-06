from functools import partial
from datetime import timedelta

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Tutor, Course
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


def CourseListCreateTests(APITestCase):
    def setUp(self):
        self.url = reverse('course-rest-api:course-list')

    def test_add_course(self):
        self.post_data = {
            'name': 'foo',
            'credits': 30,
            'duration': timedelta(days=30),
            'tutors': [{'name': 'John Doe'}]
        }
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Tutor.objects.count(), 1)
        course = Course.objects.first()
        self.compare_course(course, self.post_data)
        self.assertEqual(course.tutors.first().name, self.post_data['tutors'][0]['name'])
