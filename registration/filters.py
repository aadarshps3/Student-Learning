import django_filters
from django import forms

from .models import *





class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = ['course', 'semester']

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = RtUser
        fields = ['course', ]
