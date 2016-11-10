from django.views.generic import TemplateView

# XXX: Add get tutor view?


class CourseList(TemplateView):
    template_name = 'course/course_list.html'
