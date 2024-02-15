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
        Returns number of courses.
        """
        # courses = obj.courses().count()    
        # if courses :
        #     html = f'<a href="/admin/voyage/course/?id__in={obj.id}">{courses}</a>'
        #     return format_html(html)
        # return 0
        courses = obj.courses()
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')
        return 0

    num_courses.short_description = "no of courses"

    def no_assignments(self, obj):
   
        assignments = obj.no_assignments()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    no_assignments.short_description = "Assignments Created"

    def assignments_graded(self, obj):
        """
        number of assignments graded by each faculty.
        """   
        assignments = obj.assignments_graded().count()    
        if assignments :
            html = f'<a href="/admin/voyage/studentassignment/?id__in={obj.id}">{assignments}</a>' 
            return format_html(html)
        return 0

    #     assignments = obj.assignments_graded()
    #     ids = [i.id for i in assignments]
    #     if assignments:
    #         html = '<a href="/admin/voyage/course/?id__in='
    #         for i in ids:
    #             html = "".join((html, f"{i},"))
    #         return format_html(html[:-1] + f'">{len(assignments)}</a>')
    #     return 0

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
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')

        return 0
    num_courses.short_description = "name of Courses"

    def num_assignments(self, obj):
        """
        number of assignments assigned to each student.
        """
        assignments = obj.assignments()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')

        return obj.assignments()

    num_assignments.short_description = "Total assignments"

    def assignments_submitted(self, obj):
        """
        number of assignments submitted by each student.
        """
        assignments = obj.assignments_submitted()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')

        return obj.assignments_submitted().count()

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

    list_display = ("name", "num_courses_used","num_assignments_used")

    def num_courses_used(self, obj):
        """
        number of courses
        """
        assignments = obj.courses()
        
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')

        return 0

    num_courses_used.short_description = "Courses Used"

    def num_assignments_used(self, obj):
        """
        assignments that use each content.
        """
        assignments = obj.assignments()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

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
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>') 
        
        return obj.courses().count()

    num_courses.short_description = "courses"

    def num_students(self, obj):
        """
        number of students in each program.
        """
        students = obj.students()
        if students:
            ids = [i.id for i in students]
            html = '<a href="/admin/voyage/student/?id__in='
            for i in ids:
                html = "".join((html, f"{i},"))
            return format_html(html[:-1] + f'">{len(students)}</a>')
        return obj.students().count()
    num_students.short_description = "Students"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Course
    """

    list_display = ("name","num_assignments", "num_completed_assignments")

    def num_assignments(self, obj):
        """
        Number of assignments in each course.
        """
        assignments_count = obj.assignment_set.count()  
        if assignments_count:
            ids = [assignment.id for assignment in obj.assignment_set.all()]  
            html = '<a href="/admin/voyage/assignment/?id__in='
            for assignment_id in ids:
                html += f"{assignment_id},"
            return format_html(html[:-1] + f'">{assignments_count}</a>')
        return 0

    num_assignments.short_description = "Assignments"

    def num_completed_assignments(self, obj):
        """
        number of assignments that are completed and graded 100%
        """
        return obj.assignment_completed().count()

    num_completed_assignments.short_description = "student graded 100%"

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    AssignmentAdmin
      """
    list_display = (
        "program",
        "course_link",
        "content",
        "due",
        "instructions",
        "rubric",
    )
    list_filter = ("course", "program")

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
        """course_link
        """
        return format_html(
            '<a href="/admin/voyage/course/{0}/change/">{1}</a>',
            obj.course.id,
            obj.course.name,
        )

    course_link.short_description = "Course"


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






    # def num_assignments(self, obj):
    #     """
    #     number of assignments in each course.
    #     """
    #     assignments = obj.assignments()
    #     if assignments:
    #         dropdown_html = "<select>"
    #         for assignment in assignments:
    #             url = reverse("admin:voyage_course_change", args=[assignment.id])
    #             content_name = (
    #                 assignment.content.name if assignment.content else "No Content"
    #             )
    #             dropdown_html += f'<option value="{url}">{content_name}</option>'
    #         dropdown_html += "</select>"
    #         return format_html(dropdown_html)

    #     return obj.assignments().count()

    # num_assignments.short_description = "Assignments"

    # def num_completed_assignments(self, obj):
    #     """
    #     number of assignments that are completed and graded 100%
    #     """
    #     return obj.assignment_completed().count()

    # num_completed_assignments.short_description = "student graded 100%"
# def num_courses(self, obj):
#         """
#         Returns number of courses.
#         """
#         courses = obj.courses()
#         ids = [i.id for i in courses]
#         if courses:
#             html = '<a href="/admin/voyage/course/?id__in='
#             for i in ids:
#                 html = "".join((html, f"{i},"))
#             return format_html(html[:-1] + f'">{len(courses)}</a>')
#         return 0
    



