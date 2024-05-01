from django.contrib.auth.forms import UserCreationForm, forms, User
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TUserCreationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    class Meta(UserCreationForm.Meta):
        model = RtUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'address', 'email', 'course',)

    def clean_email(self):
        email = self.cleaned_data["email"]

        email_qs = RtUser.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email already registered")
        return email


class TeacherUpdate(UserCreationForm):
    # username = forms.CharField()
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    class Meta(UserCreationForm.Meta):
        model = RtUser
        # fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'address', 'email', 'course',)
        fields = ('first_name', 'last_name', 'address', 'email', 'course',)

BATCH_CHOICES = [
    ('Morning batch', 'Morning batch'),
    ('Afternoon batch', 'Afternoon batch'),
]

class SUserCreationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    batch = forms.ChoiceField(choices=BATCH_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = RtUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'address', 'email', 'course', 'batch','rollno',)

    def clean_email(self):
        email = self.cleaned_data["email"]

        email_qs = RtUser.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email already registered")

        return email

    def clean_rollno(self):
        rollno = self.cleaned_data["rollno"]

        email_qs = RtUser.objects.filter(rollno=rollno)
        if email_qs.exists():
            raise forms.ValidationError("This Roll No  already registered")
        return rollno


class StudentUpdate(UserCreationForm):
    # username = forms.CharField()
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    batch = forms.ChoiceField(choices=BATCH_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = RtUser
        fields = ('first_name', 'last_name', 'address', 'email', 'course','batch', 'rollno',)


class CourseBank(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


ANSWER_CHOICES = (
    ('option1', 'option1'),
    ('option2', 'option2'),
    ('option3', 'option3'),
    ('option4', 'option4'),
)


class QuestionBank(ModelForm):
    answer = forms.ChoiceField(choices=ANSWER_CHOICES)

    class Meta:
        model = Question
        exclude = ('course',)


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class AddExamTime(forms.ModelForm):
    exam_start = forms.DateTimeField(widget=DateTimeInput)
    exam_end = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = ExamSchedule
        fields = '__all__'


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['subject','file']
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(NoteForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['subject'].queryset = Subject.objects.filter(course=request.user.course)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Rec_videos
        fields = ['subject', 'Videos']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(VideoForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['subject'].queryset = Subject.objects.filter(course=request.user.course)

class ChatForm(forms.ModelForm):
    class Meta:
        model = chats
        fields = ('desc',)

        
