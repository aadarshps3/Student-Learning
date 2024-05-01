import random
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from .filters import SubjectFilter, CourseFilter
from .forms import *
from .models import *
from registration.models import chats as chats_db


def index(request):
    return render(request, 'index.html')


@login_required()
def home(request):
    return render(request, 'admintemp/home.html')


@login_required()
def teacher_home(request):
    return render(request, 'teacher/home.html')


@login_required()
def student_home(request):
    return render(request, 'student/home.html')


@login_required()
def signup(request):
    form = TUserCreationForm()
    if request.method == 'POST':
        form = TUserCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.type = 1
            form.save()
            messages.info(request, 'Teacher Added Successfully')
            return redirect('viewteacher')
    return render(request, 'admintemp/signupT.html', {'form': form, 'name': "TEACHER's Registration Form"})


@login_required()
def signups(request):
    form = SUserCreationForm()
    if request.method == 'POST':
        form = SUserCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.type = 2
            form.save()
            messages.info(request, 'Student Added Successfully')
            return redirect('viewstudent')
    return render(request, 'admintemp/signupS.html', {'form': form, 'name': "STUDENT's Registration Form"})


@login_required()
def userview(request):
    type = request.user.type
    if type == 2:
        rollno = request.user.rollno
        name = request.user.username
        return redirect('student_home')
    elif type == 1:
        subjects = request.user.course
        name = request.user.username
        return redirect('teacher_home')
    else:
        return render(request, 'admintemp/home.html')


@login_required()
def add_shedule(request):
    form = AddExamTime()
    if request.method == 'POST':
        form = AddExamTime(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Exam Schedule Added Successfully')
            return redirect('view_schedule')
    return render(request, 'admintemp/add_exam_shedule.html', {'form': form})


@login_required()
def view_schedule(request):
    s = ExamSchedule.objects.all()
    return render(request, 'admintemp/view_schedule.html', {'schedule': s})


@login_required()
def update_schedule(request, id):
    schedule = ExamSchedule.objects.get(id=id)
    print(schedule)

    form = AddExamTime(request.POST or None, instance=schedule)
    if form.is_valid():
        form.save()
        messages.info(request, 'Exam Schesule Updated Successfully')
        return redirect('view_schedule')
    return render(request, 'admintemp/update_exam_shedule.html', {'form': form})


@login_required()
def delete_schedule(request, id):
    schedule = ExamSchedule.objects.get(pk=id)
    schedule.delete()
    messages.info(request, 'Exam Schedule Deleted Successfully')
    return redirect('view_schedule')


@login_required()
def viewteacher(request):
    teacher = RtUser.objects.filter(type=1)
    return render(request, 'admintemp/viewteacher.html', {'teacher': teacher})


@login_required()
def viewstudent(request):
    student = RtUser.objects.filter(type=2)
    courseFilter = CourseFilter(request.GET, queryset=student)
    student = courseFilter.qs
    context = {'student': student,
               'courseFilter': courseFilter
               }
    return render(request, 'admintemp/viewstudent.html', context)


@login_required()
def viewstudent_teacher(request):
    t = request.user

    student = RtUser.objects.filter(type=2, course=t.course)
    return render(request, 'teacher/viewstudent.html', {'student': student})

def viewstudent_result(request):
    t = request.user
    stud = RtUser.objects.filter(type=2, course=t.course)
    exam_data = Exam.objects.filter(student__in=stud)
    data = [i for i in exam_data if i.get_percentage() < 40.0]
    print(data)
    return render(request, 'teacher/view_tution.html', {'data': data})


@login_required()
def deletest(request, id):
    student = RtUser.objects.get(pk=id)
    student.delete()
    messages.info(request, 'Student Deleted Successfully')
    return redirect('viewstudent')


@login_required()
def deletet(request, id):
    teacher = RtUser.objects.get(pk=id)
    teacher.delete()
    messages.info(request, 'Teacher Deleted Successfully')
    return redirect('viewteacher')


@login_required()
def updatet(request, id):
    teacher = RtUser.objects.get(pk=id)
    teachern = TeacherUpdate(request.POST or None, instance=teacher)
    if teachern.is_valid():
        teachern.save()
        messages.info(request, 'Teacher Updated Successfully')
        return redirect('viewteacher')
    return render(request, 'admintemp/updateteacher.html', {'form': teachern})


@login_required()
def updatest(request, id):
    student = RtUser.objects.get(pk=id)
    studentn = StudentUpdate(request.POST or None, instance=student)
    if studentn.is_valid():
        studentn.save()
        messages.info(request, 'Student Updated Successfully')
        return redirect('viewstudent')
    return render(request, 'admintemp/updatestudent.html', {'form': studentn})


@login_required()
def addcourse(request):
    if request.method == 'POST':
        form = CourseBank(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Course Added Successfully')
            return redirect('viewcourse')
    else:
        form = CourseBank()
    return render(request, 'admintemp/addcourse.html', {'form': form})


@login_required()
def addquestion(request):
    if request.method == 'POST':
        form = QuestionBank(request.POST)
        if form.is_valid():
            qstn = form.save(commit=False)
            qstn.course = request.user.course
            qstn.save()
            messages.info(request, 'Question Added Successfully')
            return redirect('addquestion')
    else:
        form = QuestionBank()
    return render(request, 'teacher/addquestion.html', {'form': form})


@login_required()
def add_subject(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()

            messages.info(request, 'Subject Added Successfully')
            return redirect('add_subject')

    return render(request, 'admintemp/subject_add.html', {'form': form})


# AJAX
def load_subject(request):
    sem_id = request.GET.get('sem_id')
    subject = Subject.objects.filter(semester=sem_id).all()

    return JsonResponse(list(subject.values('id', 'subject')), safe=False)


@login_required()
def subject(request):
    data = Subject.objects.all().order_by('course', 'semester')
    subjectFilter = SubjectFilter(request.GET, queryset=data)
    data = subjectFilter.qs
    context = {'data': data,
               'subjectFilter': subjectFilter
               }
    return render(request, 'admintemp/subject.html', context)


@login_required()
def subject_delete(request, id):
    s = Subject.objects.get(pk=id)
    s.delete()
    messages.info(request, 'Subject Deleted Successfully')
    return redirect('subject')


@login_required()
def update_subject(request, id):
    s = Subject.objects.get(pk=id)
    form = SubjectForm(instance=s)
    if request.method == 'POST':
        form = SubjectForm(request.POST or None, instance=s)
        if form.is_valid():
            form.save()
            messages.info(request, 'Subject Updated Successfully')
            return redirect('subject')
    return render(request, 'admintemp/subject_update.html', {'form': form})


@login_required()
def viewcourse(request):
    course = Course.objects.all()
    return render(request, 'admintemp/course_view.html', {'data': course})


@login_required()
def deletecourse(request, id):
    course = Course.objects.get(pk=id)
    course.delete()
    messages.info(request, 'Course Deleted Successfully')
    return redirect('viewcourse')


@login_required()
def updatecourse(request, id):
    course = Course.objects.get(pk=id)
    coursen = CourseBank(request.POST or None, instance=course)
    if coursen.is_valid():
        coursen.save()
        messages.info(request, 'Course Updated Successfully')
        return redirect('viewcourse')
    return render(request, 'admintemp/update_course.html', {'form': coursen})


@login_required()
def courseall(request):
    data = Semester.objects.all()
    return render(request, 'student/courseall.html', {'data': data})


@login_required()
def sub_list_s(request, id):
    data = Subject.objects.filter(semester=id, course=request.user.course)
    sem = Semester.objects.get(id=id)
    return render(request, 'student/subject.html', {'data': data, 'semester': sem})


@login_required()
def coursefetch1(request, id):
    exm = ExamSchedule.objects.all().last()
    exm_start = exm.exam_start
    exm_end = exm.exam_end
    duration = exm_end - exm_start

    exm_end = exm.exam_end.strftime('%Y-%m-%d %H:%M:%S')

    start = exm.exam_start.strftime('%Y-%m-%d %H:%M:%S%p')
    end = exm.exam_end.strftime('%Y-%m-%d %H:%M:%S%p')

    n = datetime.now()
    now = n.strftime('%Y-%m-%d %H:%M %p')

    if start > now:
        messages.info(request, 'Exam not started')
        return redirect('courseall')
    elif end < now:
        messages.info(request, 'Exam Time Ended')
        return redirect('courseall')
    else:
        subject = Subject.objects.get(pk=id)
        sem = Semester.objects.get(pk=subject.semester.pk)
        course = request.user.course
        print(sem, course)
        qstn_all = Question.objects.filter(subject=subject, course=course, semester=sem)
        # print(qstn_all)
        try:
            question1 = random.sample(list(qstn_all), 10)
        except ValueError:
            messages.info(request, 'No Questions')
            return redirect('courseall')
        exm_qs = Exam.objects.filter(student=request.user, subject=subject)
        if exm_qs.exists():
            question_s = Answer.objects.filter(student=request.user, subject=subject, )[:10]
        else:
            exm = Exam.objects.create(student=request.user, course=course, subject=subject, semester=sem)

            for i in question1:
                ansr, created = Answer.objects.get_or_create(
                    student=request.user,
                    question=i,
                    course=course,
                    subject=subject,
                    semester=sem

                )

                exm.questions.add(ansr)
            question_s = Answer.objects.filter(student=request.user, subject=subject)[:5]

        if question1:
            if request.method == 'POST':
                st_ansr = request.POST.get('answer')
                qstn = request.POST.get('qstn')
                print(type(qstn))
                print(Question.objects.get(id=int(qstn)))

                exm_qs = Exam.objects.filter(student=request.user, subject=subject)
                # if exm_qs\
                # \
                #
                #
                #
                #
                #
                #
                #
                #
                #
                #
                # \\\\\\\\\\\\\
                #
                # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                #
                # \
                #
                # \
                #
                #
                #
                #
                #
                #
                #
                # \\\\\
                #
                # \\\\\\z
                # z
                # z
                # .exists():
                exm = exm_qs[0]
                q = exm.questions.get(question_id=qstn)
                if q.answer:
                    messages.info(request, 'You Have  Already Answered this Question')

                else:

                    ansr = Answer.objects.get(
                        student=request.user,
                        subject=subject,
                        question=Question.objects.get(id=int(qstn)),
                        course=course)
                    ansr.answer = st_ansr
                    ansr.checked = True
                    ansr.save()
                    print(st_ansr, ansr.question.answer)
                    if st_ansr == ansr.question.answer:
                        exm.total_marks += 1
                        exm.save()
                        print(exm.total_marks)
                    result = Result.objects.get_or_create(student=request.user, exam=exm, subject=subject)
                    result[0].total_marks = exm.total_marks
                    result[0].save()


        else:
            messages.info(request, 'no qstns')
            return redirect('courseall')

    page = request.GET.get('page', 1)

    paginator = Paginator(question_s, 1)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        messages.info(request, 'end')

    return render(request, 'student/exam.html',
                  {'questions': questions, 'course': course, 'exm_end': exm_end,
                   'exam_start': exm_start, 'duration': duration})


@login_required()
def result_student(request, id):
    course = request.user.course
    results = Exam.objects.filter(student=request.user, semester=id, course=course)
    # course = Course.objects.get(id=id)
    for result in results:
        percentage = result.get_percentage()
        print(f"Result ID: {result.id}, Percentage: {percentage:.2f}%")
    return render(request, 'student/view_result.html', {'results': results, })

def tution_view(request):
    u = request.user
    exam_data = Exam.objects.filter(student=u)
    data = [i for i in exam_data if i.get_percentage() < 40.0]
    print(data)
    return render(request,'student/view_tution.html',{'data':data})


@login_required()
def result_all_s(request):
    result = Semester.objects.all()
    return render(request, 'student/result_all.html', {'data': result})


@login_required()
def result_all(request):
    result = Semester.objects.all()
    return render(request, 'teacher/result_all.html', {'courses': result})


@login_required()
def result_teacher(request, id):
    result = Exam.objects.filter(semester=id, course=request.user.course)
    # course = Course.objects.get(id=id)
    return render(request, 'teacher/view_result.html', {'results': result, })


@login_required()
def check_answer(requets, id):
    answer = Exam.objects.get(id=id)
    return render(requets, 'student/check_answer.html', {'answers': answer})


@login_required()
def semester_list(request):
    data = Semester.objects.all()

    return render(request, 'teacher/semester.html', {'data': data})


@login_required()
def subject_list(request, id):
    data = Subject.objects.filter(course=request.user.course, semester=id)
    semester = Semester.objects.get(id=id)

    return render(request, 'teacher/subjects.html', {'data': data, 'sem': semester})


@login_required()
def coursefetch2(request, id, sem_id):
    sub = Subject.objects.get(id=id)
    sem = Semester.objects.get(id=sem_id)

    question1 = Question.objects.filter(subject=id, course=request.user.course, semester=sem)
    page = request.GET.get('page', 1)
    paginator = Paginator(question1, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'teacher/coursefetch2.html', {'questions': questions, 'sub': sub, 'sem': sem})


@login_required()
def updateq(request, id):
    question = Question.objects.get(pk=id)
    form = QuestionBank(request.POST or None, instance=question)
    if form.is_valid():
        form.save()
        messages.info(request, 'Question Updated Successfully')
        return redirect('coursefetch2', question.subject.id, question.semester.id, )
    return render(request, 'teacher/updatequestion.html', {'form': form})


@login_required()
def deleteq(request, id):
    question = Question.objects.get(pk=id)
    question.delete()
    messages.info(request, 'Question Deleted Successfully')
    return redirect('courseall2')


@login_required()
def add_semester(request):
    form = SemesterForm()
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Semester Added Successfully')
            return redirect('add_semester')
    return render(request, 'admintemp/semester_add.html', {'form': form})


@login_required()
def sem_delete(request, id):
    if request.method == 'POST':
        s = Semester.objects.get(pk=id)
        s.delete()
        messages.info(request, 'Semester Deleted Successfully')
        return redirect('semester_view')


@login_required()
def semester_view(request):
    data = Semester.objects.all()
    return render(request, 'admintemp/semester_view.html', {'data': data})

def logout_view(request):
    logout(request)
    return redirect('/')

##############Teacher upload notes########
def notes_upload(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.user = request.user  # Set the user before saving
            notes.save()
            return redirect('notes-view')
    else:
        form = NoteForm(request=request)
    return render(request, 'teacher/notes_upload.html', {'form': form})

def notes_view(request):
    data = Note.objects.filter(user=request.user)
    return render(request,'teacher/notes_view.html',{'data':data})

##############Teacher upload videos########
def videos_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.user = request.user  # Set the user before saving
            notes.save()
            return redirect('videos_view')
    else:
        form = VideoForm(request=request)
    return render(request, 'teacher/videos_upload.html', {'form': form})

def videos_view(request):
    data = Rec_videos.objects.filter(user=request.user)
    return render(request,'teacher/videos_view.html',{'data':data})

################Student notes##############
def notes_views(request):
    sub = Subject.objects.filter(course=request.user.course)
    print(sub,'ssss')
    data = Note.objects.filter(subject__in=sub)
    print(data)
    return render(request,'student/notes_view.html',{'data':data})

################Student videos##############
def videos_views(request):
    sub = Subject.objects.filter(course=request.user.course)
    print(sub,'ssss')
    data = Rec_videos.objects.filter(subject__in=sub)
    print(data)
    return render(request,'student/videos_views.html',{'data':data})

############### stu sent chat to tutor #################
def chat_add_gue(request):
    form = ChatForm()
    u = RtUser.objects.get(username=request.user)
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['desc']
            chats_db.objects.create(user=u, chat_id="admin_" + u.first_name, desc=user_input)
            return redirect('chat_view_gue')
    else:
        form = ChatForm()
    return render(request, 'student/chat_add_gue.html', {'form': form})

def chat_view_gue(request):
    # u= request.user
    # print(u)
    # chat = CHAT_GUE.objects.exclude(user=u)
    # chat1=CHAT_GUE.objects.filter(user=u)
    # print(chat1)
    u = RtUser.objects.get(username=request.user)
    id = "admin_" + u.first_name
    data = chats_db.objects.filter(chat_id=id)

    return render(request, 'student/chat_view_gue.html', {'chat': data})

################techer view chat ##############################

def chat_view_gue_admin(request):
    data = RtUser.objects.filter(type=2)
    return render(request, 'teacher/chat_view_gue_admin.html', {'data': data})


def view_chat_Emp(request, first_name):
    print(first_name)
    request.session['chat_name'] = first_name
    data = RtUser.objects.filter(type=2)
    chats = chats_db.objects.filter(chat_id="admin_" + first_name)

    return render(request, 'teacher/chat_view_gue_admin.html', {'chats': chats, 'data': data})


def chat_add_ad_gu(request):
    form = ChatForm()
    u = request.user

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            Name = request.session['chat_name']
            user_input = form.cleaned_data['desc']
            print(user_input, ">>>>>>>>>>>>>>>>>")
            chats_db.objects.create(user="admin", chat_id="admin_" + Name, desc=user_input)
            # obj = form.save(commit=False)
            # obj.user = u
            # obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('chat_view_gue_admin')
    else:
        form = ChatForm()
    return render(request, 'teacher/chat_add_ad_gu.html', {'form': form})
