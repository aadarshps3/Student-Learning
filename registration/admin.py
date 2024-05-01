from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(RtUser)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(ExamSchedule)
admin.site.register(Subject)