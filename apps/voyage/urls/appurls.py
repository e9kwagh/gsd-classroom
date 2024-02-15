from django.urls import path


from ..views.appviews import FacultyView,StudentPageView,FacultyPageView,StudentCoursesView,VoyageDefaultView,CreateAssignment,CreateCourse

urlpatterns = [
    path("", VoyageDefaultView.as_view(), name="home"),
    path("dashboard/faculty/<int:f_id>", FacultyView.as_view(), name="faculty"),
    path("dashboard/student/<int:s_id>", StudentCoursesView.as_view(), name="student"),
    path('courseform', CreateCourse.as_view(), name='courseform'),
    path('assignmentform/', CreateAssignment.as_view(), name="assignmentform"),
    path("facultypage/", FacultyPageView.as_view(), name="facultypage"),
    path("Studentpage/", StudentPageView.as_view(), name="Studentpage"),

    
]