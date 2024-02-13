from django.contrib import admin

from .models import (
    Faculty,
    Content,
    Program,
    Course,
    Student,
    Assignment,
    StudentAssignment,
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id","user","github","is_active")
  
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
     list_display = ("user","github","is_active","program")


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
     list_display = ["name"]

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name","start","end")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("program","course","content","due","instructions","rubric")

   
@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
        list_display = ("student","assignment","grade","submitted","reviewed","reviewer","feedback")



