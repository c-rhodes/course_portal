from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'getCourse/$', views.CourseDetailAPIView.as_view(), name='get-course'),
    url(r'getAllCourses/$', views.CourseListAPIView.as_view(), name='get-courses'),
    url(r'searchCourse/$', views.CourseSearchAPIView.as_view(), name='search-course'),
    url(r'addCourse/$', views.CourseCreateAPIView.as_view(), name='add-course'),
]
