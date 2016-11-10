from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CourseList.as_view(), name='course-list'),
]
