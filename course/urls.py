from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'getCourse/$', views.CourseDetail.as_view(), name='get-course'),
    url(r'getAllCourses/$', views.CourseList.as_view(), name='get-courses'),
    url(r'searchCourse/$', views.CourseSearch.as_view(), name='search-course'),
    url(r'addCourse/$', views.CourseCreate.as_view(), name='add-course'),
]
