from django.views.generic import TemplateView

from .forms import AddCourseForm, SearchCourseForm, ListCourseForm

# XXX: Add get tutor view?


class RestAPIDemoHome(TemplateView):
    template_name = 'course/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_course_form'] = AddCourseForm
        context['course_search_form'] = SearchCourseForm
        context['course_list_form'] = ListCourseForm
        return context
