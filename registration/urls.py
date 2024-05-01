from django.urls import path

from registration import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('registerteacher/',views.signup,name='register'),
    path('registerstudent/',views.signups,name='registerstudent'),
    path('userview/',views.userview,name='userview'),
    path('viewteacher/',views.viewteacher,name='viewteacher'),
    path('teacher_home/',views.teacher_home,name='teacher_home'),
    path('student_home/',views.student_home,name='student_home'),
    path('add_shedule/',views.add_shedule,name='add_shedule'),
    path('view_schedule/',views.view_schedule,name='view_schedule'),
    path('update_schedule/<int:id>/',views.update_schedule,name='update_schedule'),
    path('delete_schedule/<int:id>/',views.delete_schedule,name='delete_schedule'),
    path('viewstudent/',views.viewstudent,name='viewstudent'),
    path('deletest/<int:id>',views.deletest,name='deletest'),
    path('deletet/<int:id>',views.deletet,name='deletet'),
    path('updatet/<int:id>',views.updatet,name='updatet'),
    path('updatest/<int:id>',views.updatest,name='updatest'),
    path('sign-out/',views.logout_view,name='sign-out'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('addquestion/',views.addquestion,name='addquestion'),
    path('addcourse/',views.addcourse,name='addcourse'),
    path('viewcourse/',views.viewcourse,name='viewcourse'),
    path('deletecourse/<int:id>',views.deletecourse,name='deletecourse'),
    path('updatecourse/<int:id>/',views.updatecourse,name='updatecourse'),
    path('courseall',views.courseall,name='courseall'),
    # path('courseall2',views.courseall2,name='courseall2'),
    path('coursefetch1/<int:id>/',views.coursefetch1,name='coursefetch1'),

    path('updateq/<int:id>',views.updateq,name='updateq'),
    path('deleteq/<int:id>',views.deleteq,name='deleteq'),
    path('result_student/<int:id>/',views.result_student,name='result_student'),
    path('tution-view/',views.tution_view,name='tution-view'),
    path('result_teacher/<int:id>/',views.result_teacher,name='result_teacher'),
    path('check_answer/<int:id>',views.check_answer,name='check_answer'),
    path('viewstudent_teacher',views.viewstudent_teacher,name='viewstudent_teacher'),
    path('viewstudent-result',views.viewstudent_result,name='viewstudent-result'),
    path('result_all',views.result_all,name='result_all'),
    path('result_all_s',views.result_all_s,name='result_all_s'),
    path('add_semester',views.add_semester,name='add_semester'),
    path('semester_view',views.semester_view,name='semester_view'),
    path('sem_delete/<int:id>/',views.sem_delete,name='sem_delete'),
    path('add_subject/',views.add_subject,name='add_subject'),
    path('subject/',views.subject,name='subject'),
    path('update_subject/<int:id>/',views.update_subject,name='update_subject'),
    path('subject_delete/<int:id>/',views.subject_delete,name='subject_delete'),
    path('coursefetch2/<int:id>/<int:sem_id>/', views.coursefetch2, name='coursefetch2'),


    path('semester_list/',views.semester_list,name='semester_list'),
    path('sub_list_s/<int:id>/',views.sub_list_s,name='sub_list_s'),
    path('subject_list/<int:id>/',views.subject_list,name='subject_list'),
    path('ajax/load-subject/', views.load_subject, name='ajax_load_subject'),  # AJAX

    path('notes-upload/',views.notes_upload,name='notes-upload'),
    path('notes-view/',views.notes_view,name='notes-view'),
    path('notes-view-st/',views.notes_views,name='notes-view-st'),

    path('videos_upload',views.videos_upload,name='videos_upload'),
    path('videos_view',views.videos_view,name='videos_view'),

    path('videos_views',views.videos_views,name='videos_views'),

    path('chat_add_gue',views.chat_add_gue,name='chat_add_gue'),
    path('chat_view_gue',views.chat_view_gue,name='chat_view_gue'),

    path('chat_view_gue_admin',views.chat_view_gue_admin,name='chat_view_gue_admin'),
    path('view_chat_Emp/<first_name>/',views.view_chat_Emp,name='view_chat_Emp'),
    path('chat_add_ad_gu',views.chat_add_ad_gu,name='chat_add_ad_gu'),






]
