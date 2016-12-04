from functools import partial
from datetime import timedelta

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Tutor, Course
from course.factories import TutorFactory, CourseFactory
from course_http_api.tests.test_views import CommonTestMixin


class CourseDetailTests(APITestCase, CommonTestMixin):
    def setUp(self):
        self.url = partial(reverse, 'course-rest-api:course-detail')

    def test_get_course(self):
        tutor = TutorFactory()
        course = CourseFactory(tutors=[tutor])
        response = self.client.get(self.url(kwargs=dict(pk=course.pk)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.format_course(course, tutor))

    def test_update_course(self):
        tutor = TutorFactory()
        course = CourseFactory(tutors=[tutor])
        tutor_2 = TutorFactory()
        post_data = {
            'name': 'foo',
            'credits': 100,
            'duration': timedelta(1),
            'tutors': [{'id': tutor_2.pk}]
        }
        response = self.client.patch(self.url(kwargs=dict(pk=course.pk)), post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(course.tutors.count(), 1)
        self.compare_course(course, post_data)
        self.assertEqual(course.tutors.first(), tutor_2)

    def test_delete_course(self):
        course = CourseFactory()
        response = self.client.delete(self.url(kwargs=dict(pk=course.pk)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class CourseListCreateTests(APITestCase, CommonTestMixin):
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
