"""modules"""
from django.urls import reverse
from django.utils.html import format_html
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
    """
    Faculty
    """

    list_display = (
        "id",
        "user",
        "github",
        "num_courses",
        "no_assignments",
        "assignments_graded",
    )

    def num_courses(self, obj):
        """
        number of courses taught by each faculty.
        """
        return obj.courses()

    num_courses.short_description = "no of courses"

    def no_assignments(self, obj):
        """
        number of assignments created by each faculty.
        """
        return obj.no_assignments()

    no_assignments.short_description = "Assignments Created"

    def assignments_graded(self, obj):
        """
        number of assignments graded by each faculty.
        """
        return obj.assignments_graded()

    assignments_graded.short_description = " assignments graded"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Student
    """

    list_display = (
        "id",
        "user",
        "github",
        "is_active",
        "program",
        "num_courses",
        "num_assignments",
        "assignments_submitted",
        "average_grade",
    )

    def num_courses(self, obj):
        """
        number of courses each student is enrolled.
        """
      
        courses = obj.courses()
        if courses:
            dropdown_html = '<select>'
            for course in courses:
                url = reverse("admin:voyage_course_change", args=[course.id])
                dropdown_html += f'<option value="{url}">{course.name}</option>'
            dropdown_html += '</select>'
            return format_html(dropdown_html)
   

    num_courses.short_description = "name of Courses"

    def num_assignments(self, obj):
        """
        number of assignments assigned to each student.
        """
        assignments = obj.assignments()
        if assignments:
            dropdown_html = '<select>'
            for assignment in assignments:
                url = reverse("admin:voyage_course_change", args=[assignment.id])
                dropdown_html += f'<option value="{url}">{assignment.content.name}</option>'
            dropdown_html += '</select>'
            return format_html(dropdown_html)
        
        return obj.assignments()


    num_assignments.short_description = "Total assignments"

    def assignments_submitted(self, obj):
        """
        number of assignments submitted by each student.
        """
        return obj.assignments_submitted()

    assignments_submitted.short_description = "Assignments Submitted"

    def average_grade(self, obj):
        """
        average grade of each student.
        """
        return obj.average_grade()

    average_grade.short_description = "Avg Grade"


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Content
    """

    list_display = ["name"]

    def num_courses_used(self, obj):
        """
        number of courses
        """
        return obj.courses()

    num_courses_used.short_description = "Courses Used"

    def num_assignments_used(self, obj):
        """
        assignments that use each content.
        """
        return obj.assignments()

    num_assignments_used.short_description = "Assignments Used"


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Program
    """

    list_display = ("name", "num_courses", "num_students")

    def num_courses(self, obj):
        """
        number of courses in each program.
        """
         
        courses = obj.courses()
        if courses:
            dropdown_html = '<select>'
            for course in courses:
                url = reverse("admin:voyage_course_change", args=[course.id])
                content_name = course.content.name if course.content else 'No Content'
                dropdown_html += f'<option value="{url}">{content_name}</option>'
            dropdown_html += '</select>'
            return format_html(dropdown_html)
        
        return obj.courses().count()


    num_courses.short_description = "courses"

    def num_students(self, obj):
        """
        number of students in each program.
        """
        students =  obj.students()
        if students:
            dropdown_html = '<select>'
            for student in students:
                url = reverse("admin:voyage_course_change", args=[student.id])
                student_name = student.user.username if student.user else 'No User'
                dropdown_html += f'<option value="{url}">{student_name}</option>'
            dropdown_html += '</select>'
            return format_html(dropdown_html)
        
        return obj.students().count()

    num_students.short_description = "Students"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Course
    """

    list_display = ("name", "num_assignments", "num_completed_assignments")

    def num_assignments(self, obj):
        """
        number of assignments in each course.
        """
        assignments = obj.assignments()
        if assignments:
            dropdown_html = '<select>'
            for assignment in assignments:
                url = reverse("admin:voyage_course_change", args=[assignment.id])
                content_name = assignment.content.name if assignment.content else 'No Content'
                dropdown_html += f'<option value="{url}">{content_name}</option>'
            dropdown_html += '</select>'
            return format_html(dropdown_html)
        
        return obj.assignments().count()



     

    num_assignments.short_description = "Assignments"

    def num_completed_assignments(self, obj):
        """
        number of assignments that are completed and graded 100%
        """
        return obj.assignment_completed().count()

    num_completed_assignments.short_description = "student graded 100%"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('program', 'course_link', 'content', 'due', 'instructions', 'rubric')
    list_filter = ('course', 'program')

    # def num_assignments(self, obj):
    #     """
    #     number of assignments in each course.
    #     """
    #     assignments = obj.assignments()
    #     if assignments:
    #         dropdown_html = '<select>'
    #         for assignment in assignments:
    #             url = reverse("admin:voyage_course_change", args=[assignment.id])
    #             content_name = assignment.content.name if assignment.content else 'No Content'
    #         dropdown_html += '</select>'
    #         return format_html(dropdown_html)
        
    #     return obj.assignments().count()


    def course_link(self, obj):

        return format_html('<a href="/admin/voyage/course/{0}/change/">{1}</a>', obj.course.id, obj.course.name)
    course_link.short_description = 'Course'

    # courses = obj.courses()
    #         if courses:
    #             dropdown_html = '<select>'
    #             for course in courses:
    #                 url = reverse("admin:voyage_course_change", args=[course.id])
    #                 dropdown_html += f'<option value="{url}">{course.name}</option>'
    #             dropdown_html += '</select>'
    #             return format_html(dropdown_html)
   



@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    StudentAssignment
    """

    list_display = (
        "student",
        "assignment",
        "grade",
        "submitted",
        "reviewed",
        "reviewer",
        "feedback",
    )





# PS C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom> black apps
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\apps.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\urls\appurls.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\admin.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\views\appviews.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\models.py
