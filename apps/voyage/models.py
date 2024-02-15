"""models.py"""

import random
from datetime import timedelta
from faker import Faker
from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel


class Faculty(QuxModel):
    """Faculty"""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def random_faculty(cls):
        """random_faculty"""
        faker = Faker()
        for _ in range(5):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()

            user = get_user_model().objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            Faculty.objects.create(
                user=user, github=f"https://github.com/{username}", is_active=True
            )



    def programs(self):
        """
        programs
        """
        return Program.objects.filter(
            student__studentassignment__reviewer=self
        ).distinct()

    
    def courses(self):
        """
        Show the number of courses each faculty is teaching
        """
        # return self.content_set.filter(assignment__isnull=False).distinct().count()
        return Assignment.objects.filter(content__faculty=self)

    def assignments_graded(self, assignment=None):
        """
        Show the number of assignments graded by each faculty
        """
        if assignment:
            return StudentAssignment.objects.filter(
                reviewer=self, assignment=assignment
            )
        return StudentAssignment.objects.filter(reviewer=self)

    def no_assignments(self):
        """
        Show the number of assignments by each faculty
        """

        return Assignment.objects.filter(content__faculty=self).distinct()

    def content(self, program=None, course=None):
        """
        content of  programs or courses of  faculty.
        """
        contents = self.content_set.all()

        if program and course:
            final = set()
            for content in contents:
                assignments = content.assignment_set.filter(
                    program=program, course=course
                )
                if assignments:
                    final.add(content)
            contents = final
        elif program:
            final = set()
            for content in contents:
                assignments = content.assignment_set.filter(program=program)
                if assignments:
                    final.add(content)
            contents = final
        elif course:
            final = set()
            for content in contents:
                assignments = content.assignment_set.filter(course=course)
                if assignments:
                    final.add(content)
            contents = final

        return contents


class Program(QuxModel):
    """
    Example: Cohort-2
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    @classmethod
    def random_program(cls):
        """random_program"""
        faker = Faker()
        for _ in range(3):
            name = faker.first_name()
            start = faker.date_time_this_decade(tzinfo=None) + timedelta(
                days=faker.random_int(min=1, max=365)
            )
            end = start + timedelta(days=faker.random_int(min=1, max=365))
            Program.objects.create(name=name, start=start, end=end)

    def __str__(self):
        """str"""
        return f"{self.name}"

    def students(self):
        """
        List of students in the program
        """
        return self.student_set.all()

    def courses(self):
        """
        number of courses in each program.
        """
        # li = set(
        #     course
        #     for course in Course.objects.all()
        #     if self.assignment_set.filter(course__in = course)
        # )

        li = self.assignment_set.filter(course__in=Course.objects.all())
        return li


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    @classmethod
    def random_course(cls):
        """random_course"""
        faker = Faker()
        for _ in range(3):
            name = faker.first_name()
            Course.objects.create(name=name)

    def __str__(self):
        return f"{self.name}"

    def programs(self):
        """
        returns programs associated with this course
        """
        assignments = self.assignment_set.all()
        return Program.objects.filter(assignment__in=assignments).distinct()

    @property
    def students(self):
        """
        students related with this course
        """

        # programs = [assignment.program for assignment in self.assignment_set.all()]
        # students = []
        # for program in programs:
        #     students.append(list(program.student_set.all()))
        # return list(set(students))

        return Assignment.objects.filter(
            program__student__program__isnull=False, course=self
        )

    def content(self):
        """
        all content in this course
        """

        return set(assignment.content for assignment in self.assignment_set.all())
        
    @property
    def assignments(self):
        """
        assignments related with this course
        """
        return Assignment.objects.filter(course=self)
        #return self.assignment_set.all()

  
    def assignment_completed(self):
        """
        Total number of assignments that are completed and graded 100
        """
        return StudentAssignment.objects.filter(submitted__isnull=False, grade__gte=100)


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"

    @classmethod
    def random_content(cls):
        """random_content"""
        faker = Faker()
        for i in range(28):
            f_id = int(random.sample(range(2, 6), 1)[0])
            repo = f"https://github.com/{i}"
            Content.objects.create(
                name=faker.first_name(), faculty=Faculty.objects.get(pk=f_id), repo=repo
            )

    
    def courses(self):
        """
        Show the number of courses that use each content
        """
        return Course.objects.filter(assignment__content=self).distinct()

    def assignments(self):
        """
        all assignments with content.
        """
        return self.assignment_set.all()


class Student(QuxModel):
    """Student"""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    @classmethod
    def random_student(cls):
        """random_student"""
        faker = Faker()
        for _ in range(10):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name = faker.last_name()
            email = faker.email()

            user = get_user_model().objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            pro_id = int(random.sample(range(1, 3), 1)[0])
            program = Program.objects.get(pk=pro_id)
            Student.objects.create(
                user=user,
                github=f"https://github.com/{username}",
                is_active=True,
                program=program,
            )
   
    def courses(self):
        """courses related with program"""
        # return Course.objects.none()
        return set(
            assignment.course for assignment in self.program.assignment_set.all()
        )

    def assignments(self):
        """
        all assignments associated with the student's program.
        """
        # return Assignment.objects.none()
        return self.program.assignment_set.all()
    
    def assignments_submitted(self, assignment=None):
        """submitted assignments"""
        
        if assignment:
            return StudentAssignment.objects.filter(
                assignment=assignment, student=self, submitted__isnull=False
            )
        return StudentAssignment.objects.filter(
            student=self, submitted__isnull=False
        )

    def assignments_not_submited(self, assignment=None):
        """assignments not submitted"""
        if assignment:
            return Assignment.objects.exclude(
                studentassignment__student=self,
                studentassignment__assignment=assignment,
                studentassignment__submitted__isnull=False,
            )
        return Assignment.objects.exclude(
            studentassignment__student=self, studentassignment__submitted__isnull=False
        )
    

    
    def assignments_graded(self, assignment=None):
        """
        check the grade of assignments
        """
        if assignment:
            return StudentAssignment.objects.filter(
                grade__isnull=False, student=self, assignment=assignment
            )
        return self.studentassignment_set.filter(
            submitted__isnull=False, grade__isnull=False
        )
    

    @property
    def average_grade(self):
        """
        students average grade
        """
        submitted_assignments = self.studentassignment_set.filter(
            submitted__isnull=False
        )
        try:
            total_assignments = self.studentassignment_set.all().count()
            total_grade = sum(assignment.grade for assignment in submitted_assignments)
            avg = int(total_grade // total_assignments)
            return avg
        except ZeroDivisionError:
            return 0


class Assignment(QuxModel):
    """Assignment"""

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    @classmethod
    def random_assignment(cls):
        """random_assignment"""
        faker = Faker()
        for _ in range(5):

            rubric = faker.name()
            instructions = faker.last_name()
            pro_id = int(random.sample(range(1, 3), 1)[0])
            con_id = int(random.sample(range(1, 28), 1)[0])
            program = Program.objects.get(pk=pro_id)
            content = Content.objects.get(pk=con_id)
            course = Course.objects.get(pk=pro_id)
            due = faker.date_time_between_dates(
                datetime_start=program.start, datetime_end=program.end, tzinfo=None
            )
            Assignment.objects.create(
                due=due,
                course=course,
                content=content,
                program=program,
                instructions=instructions,
                rubric=rubric,
            )

    class Meta:
        """Meta"""

        unique_together = ["program", "course", "content"]

    def __str__(self):
        """str"""
        return self.content.name

    def students(self):
        """
        student assignments
        """
        return Student.objects.filter(studentassignment__assignment=self)

    
    @property
    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        if graded:
            return self.studentassignment_set.filter(grade__isnull=False)
        if not graded:
            return self.studentassignment_set.filter(grade__isnull=True)
        return self.studentassignment_set.all()
    

    @property
    def avg(self):
        """
        average grades of  assignment.
        """
        submissions = self.studentassignment_set.filter(grade__isnull=False)
        try :
            assignment = self.studentassignment_set.all().count()
            total_grade = sum(submission.grade for submission in submissions)
            avg = total_grade // assignment
            return avg
        except ZeroDivisionError:
            return 0

class StudentAssignment(QuxModel):
    """StudentAssignment"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    submitted = models.DateTimeField(default=None, null=True, blank=True)
    reviewed = models.DateTimeField(default=None, null=True, blank=True)
    reviewer = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, default=None, null=True, blank=True
    )
    feedback = models.TextField(default=None, null=True, blank=True)

    @classmethod
    def random_assignment(cls):
        """random_assignment"""
        faker = Faker()
        for _ in range(5):
            stud_id = int(random.sample(range(1, 10), 1)[0])
            a_id = int(random.sample(range(1, 5), 1)[0])
            grade = random.uniform(30, 100)
            assignment = Assignment.objects.get(pk=a_id)
            student = Student.objects.get(pk=stud_id)
            reviewer = Faculty.objects.get(pk=a_id)
            feedback = faker.text()
            pro_id = int(random.sample(range(1, 3), 1)[0])
            program = Program.objects.get(pk=pro_id)
            submitted = faker.date_time_between_dates(
                datetime_start=program.start, datetime_end=program.end, tzinfo=None
            )
            reviewed = faker.date_time_between_dates(
                datetime_start=submitted, datetime_end=program.end, tzinfo=None
            )
            StudentAssignment.objects.create(
                grade=grade,
                assignment=assignment,
                student=student,
                submitted=submitted,
                reviewer=reviewer,
                feedback=feedback,
                reviewed=reviewed,
            )
