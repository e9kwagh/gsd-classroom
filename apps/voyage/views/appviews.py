"""appsview.py"""

from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from apps.voyage.models import Faculty, Course, Assignment, Student
from django.http import HttpResponse
from apps.voyage.forms import CourseForm, AssignmentForm
from qux.seo.mixin import SEOMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class VoyageDefaultView(SEOMixin, TemplateView):
    """
    VoyageDefaultView
    """

    template_name = "voyage/index.html"


class FacultyView(ListView):
    """
    FacultyView
    """

    template_name = "voyage/faculty.html"
    model = Faculty

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        f_id = self.kwargs["f_id"]
        try:
            faculty = Faculty.objects.get(id=f_id)
            courses = faculty.courses()
            if not courses:
                context["message"] = "Faculty has no students."
            context["courses"] = courses
            context["page"] = "faculty"
        except Faculty.DoesNotExist:
            context["message"] = "Faculty does not exist"
        context["page"] = "faculty"
        return context


class StudentCoursesView(ListView):
    """
    StudentCoursesView
    """

    template_name = "voyage/faculty.html"
    model = Assignment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s_id = self.kwargs["s_id"]
        try:
            student = Student.objects.get(id=s_id)
        except Faculty.DoesNotExist:
            context["message"] = "student does not exist"

        courses = student.courses()
        assignments = student.assignments()
        submissions = student.assignments_submitted()

        if not courses:
            context["message"] = "student has no courses."

        context["courses"] = courses
        context["assignments"] = assignments
        context["submissions"] = submissions
        context["page"] = "Student"

        return context


class FacultyPageView(ListView):
    """
    faculty page
    """

    template_name = "voyage/facultyView.html"
    model = Faculty
    context_object_name = "faculties"


class CreateCourse(TemplateView):
    """
    new course form
    """

    template_name = "voyage/create_form.html"

    def get_context_data(self, **kwargs):
        """
        get_context_data
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context

    def post(self, request, **kwargs):
        """
        post request
        """
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("facultypage"))
        return render(request, self.template_name, {"form": form})


class StudentPageView(ListView):
    """
    studentView
    """

    model = Student
    template_name = "voyage/studentView.html"
    context_object_name = "students"


class CreateAssignment(TemplateView):
    """
    createassignment
    """

    template_name = "voyage/create_form.html"

    def get_context_data(self, **kwargs):
        """
        get_context_data
        """
        context = super().get_context_data(**kwargs)
        context["form"] = AssignmentForm()
        return context

    def post(self, request, **kwargs):
        """
        post
        """
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("Studentpage"))
        return render(request, self.template_name, {"form": form})


# class StudentAssignmentsView(ListView):
#     """
#     StudentAssignmentsView
#     """
#     template_name = "voyage/faculty.html"
#     model = Sudent

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         s_id = self.kwargs["s_id"]
#         try:
#             faculty = Faculty.objects.get(id=s_id)
#             courses = faculty.courses()
#             if not courses:
#                 context["message"] = "Faculty has no students."
#             else:
#                 context["courses"] = courses
#                 context["id"] = f_id
#                 context["page"] = "faculty"
#         except Faculty.DoesNotExist:
#             context["message"] = "Faculty does not exist"
#         return context


# class StudentSubmissionsView(ListView):
#     """
#     FacultyView
#     """
#     template_name = "voyage/faculty.html"
#     model = Faculty

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         f_id = self.kwargs["f_id"]
#         try:
#             faculty = Faculty.objects.get(id=f_id)
#             courses = faculty.courses()
#             if not courses:
#                 context["message"] = "Faculty has no students."
#             else:
#                 context["courses"] = courses
#                 context["id"] = f_id
#                 context["page"] = "faculty"
#         except Faculty.DoesNotExist:
#             context["message"] = "Faculty does not exist"
#         return context


# class FacultyView(ListView):
#     template_name = "voyage/faculty.html"
#     model = Course

# class StudentCoursesView(ListView):
#     template_name = "voyage/faculty.html"
#     model = Course

# class StudentAssignmentsView(ListView):
#     template_name = "voyage/faculty.html"
#     model = Assignment