from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Course(models.Model):
    coursename = models.CharField(max_length=20)
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return f"{self.coursename}"


class Semester(models.Model):
    semester_name = models.CharField(max_length=200)

    def __str__(self):
        return self.semester_name


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class RtUser(AbstractUser):
    first_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=200)
    type = models.IntegerField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    rollno = models.IntegerField(null=True)
    batch = models.CharField(max_length=20,null=True)


class ExamSchedule(models.Model):
    # date = models.DateField()
    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return self.question


class Answer(models.Model):
    student = models.ForeignKey(RtUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='ansr')
    answer = models.CharField(max_length=20, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    checked = models.BooleanField(default=False)


class Exam(models.Model):
    student = models.ForeignKey(RtUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=0)
    questions = models.ManyToManyField(Answer)

    def get_total_question(self):
        return self.questions.all().count()

    def get_percentage(self):
        qstns = self.questions.all().count()
        return (self.total_marks / qstns) * 100


class Result(models.Model):
    student = models.ForeignKey(RtUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='result')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=0)

class Note(models.Model):
    user = models.ForeignKey(RtUser,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    file = models.FileField(upload_to='notes/')

class Rec_videos(models.Model):
    user = models.ForeignKey(RtUser,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    Videos = models.FileField(upload_to='video/')


class chats(models.Model):
    user=models.CharField(max_length=100)
    chat_id=models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.user
# from django.utils.timezone import utc
# from datetime import datetime, time

# def time_diff(self):
#     t1 = datetime.datetime.strptime(str(self.exam_start), '%H:%M:%S')
#     t2 = datetime.datetime.strptime(str(self.exam_end), '%H:%M:%S')
#     dt = abs(t2 - t1)
#     return datetime.time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime('%H:%M:%S')
