from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from course.models import Course
from course.serializers import CourseSerializer


class CourseDetailAPIView(APIView):

    def get(self, request, format=None):
        try:
            course_name = request.GET['coursename']
            course = Course.objects.get(name=course_name)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data)


class CourseSearchAPIView(APIView):

    def get(self, request, format=None):
        try:
            course_name = request.GET['coursename']
            courses = Course.objects.filter(name__icontains=course_name)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
