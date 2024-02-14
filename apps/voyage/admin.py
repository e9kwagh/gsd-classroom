"""modules"""

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

    list_display = ("id", "user", "github", "is_active")

    def num_courses(self, obj):
        """
        number of courses taught by each faculty.
        """
        return obj.courses()

    num_courses.short_description = "Courses "

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

    assignments_graded.short_description = " Graded"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Student
    """

    list_display = ("user", "github", "is_active", "program")

    def num_courses(self, obj):
        """
        number of courses each student is enrolled.
        """
        return obj.courses()

    num_courses.short_description = "Courses"

    def num_assignments(self, obj):
        """
        number of assignments assigned to each student.
        """
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
        return obj.courses()

    num_courses.short_description = "Courses"

    def num_students(self, obj):
        """
        number of students in each program.
        """
        return obj.students()

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
        return obj.assignments()

    num_assignments.short_description = "Assignments"

    def num_completed_assignments(self, obj):
        """
        number of assignments that are completed and graded 100%
        """
        return obj.assignment_completed()

    num_completed_assignments.short_description = "Completed Assignments"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment
    """

    list_display = ("program", "course", "content", "due", "instructions", "rubric")


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
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\migrations\0002_alter_assignment_unique_together.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\urls\appurls.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\admin.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\views\appviews.py
# reformatted C:\Users\Kunal Wagh\Desktop\ie9\GSD\gsd-classroom\apps\voyage\models.py
