from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Course

format_choices = (
    ('json', 'json'),
    ('xml', 'xml'),
    ('text', 'text')
)


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'course-create-form'
        self.helper.form_action = reverse('course-rest-api:course-list')
        self.helper.add_input(Submit('submit', 'Submit'))


class SearchCourseForm(forms.ModelForm):
    format = forms.ChoiceField(choices=format_choices)

    class Meta:
        model = Course
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'course-search-form'
        self.helper.add_input(Submit('search', 'Search'))


class ListCourseForm(forms.Form):
    format = forms.ChoiceField(choices=format_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'course-list-form'
        self.helper.add_input(Submit('submit', 'Submit'))
