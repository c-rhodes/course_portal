from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer


class CourseDetail(APIView):

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


class CourseSearch(APIView):

    def get(self, request, format=None):
        try:
            course_name = request.GET['coursename']
            courses = Course.objects.filter(name__icontains=course_name)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseCreate(generics.CreateAPIView):
    serializer_class = CourseSerializer


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# XXX: Add get tutor view?
