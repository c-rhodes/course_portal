from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tutor(models.Model):
    name = models.CharField(
        _('Name of tutor'), max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(
        _('Name of course'), max_length=255, unique=True)
    credits = models.PositiveIntegerField()
    duration = models.DurationField()
    tutors = models.ManyToManyField(Tutor)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.name
