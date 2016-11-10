from datetime import timedelta
from urllib.parse import urlencode

from django.urls import reverse
from django.utils.duration import duration_string

from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Tutor, Course
from course.factories import TutorFactory, CourseFactory


class CommonTestMixin:
    """Mixin providing common test utilities"""
    def url_format(self, **kwargs):
        """Helper function for url formatting"""
        return '{}?{}'.format(self.url, urlencode(kwargs))

    def format_course(self, course, tutor):
        """Format course object into the expected api response json"""
        course_format = {
            'id': course.pk,
            'name': course.name,
            'credits': course.credits,
            # django-rest-framework uses django.utils.duration.duration_string for duration field serialization
            # https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/fields.py#L1289
            'duration': duration_string(course.duration),
            'tutors': [
                {
                    'id': tutor.pk,
                    'name': tutor.name
                }
            ]
        }
        return course_format

    def compare_course(self, course_object, course_dict):
        """Compare Course object against dict containing course values"""
        self.assertEqual(course_object.name, course_dict['name'])
        self.assertEqual(course_object.credits, course_dict['credits'])
        self.assertEqual(course_object.duration, course_dict['duration'])


class TestCourseDetail(APITestCase, CommonTestMixin):
    def setUp(self):
        self.url = reverse('course-http-api:get-course')

    def test_get_course_bad_request(self):
        """Expect a response status code of 400 for a request with invalid query parameters"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_course_does_not_exist(self):
        """Expect a response status code of 404 if course does not exist"""
        response = self.client.get(self.url_format(coursename='foo'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_course(self):
        """Test a course object is returned"""
        tutor = TutorFactory()
        course = CourseFactory(tutors=[tutor])
        response = self.client.get(self.url_format(coursename=course.name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.format_course(course, tutor))


class TestCourseSearch(APITestCase, CommonTestMixin):
    def setUp(self):
        self.url = reverse('course-http-api:search-course')

    def test_get_course_bad_request(self):
        """Expect a response status code of 400 for a request with invalid query parameters"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_course(self):
        """Test course objects matching query are returned"""
        # Create test data
        tutor = TutorFactory()
        # Create 2 courses to search against (coursename will be course[0-9]+)
        courses = [CourseFactory(tutors=[tutor]) for i in range(2)]
        CourseFactory(name='foo')  # Create a third course 'foo' that shouldn't match the search parameters
        response = self.client.get(self.url_format(coursename='course'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [self.format_course(course, tutor) for course in courses]
        self.assertEqual(response.json(), expected_response)


class TestCourseCreate(APITestCase, CommonTestMixin):
    def setUp(self):
        self.url = reverse('course-http-api:add-course')
        self.post_data = {
            'name': 'foo',
            'credits': 30,
            'duration': timedelta(days=30),
            'tutors': [{'name': 'John Doe'}]
        }

    def test_course_create_new_tutor(self):
        """Test course is created with new tutor"""
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Tutor.objects.count(), 1)
        course = Course.objects.first()
        self.compare_course(course, self.post_data)
        self.assertEqual(course.tutors.first().name, self.post_data['tutors'][0]['name'])

    def test_course_create_existing_tutor(self):
        """Test course is created using existing tutor"""
        # Create tutor
        tutor = TutorFactory()
        self.assertEqual(Tutor.objects.count(), 1)
        self.post_data['tutors'] = [{'id': tutor.id}]
        response = self.client.post(self.url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Tutor.objects.count(), 1)
        course = Course.objects.first()
        self.compare_course(course, self.post_data)
        course_tutor = course.tutors.first()
        self.assertEqual(course_tutor.name, tutor.name)
        self.assertEqual(course_tutor.id, tutor.id)
