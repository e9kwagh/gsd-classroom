from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel
from faker import Faker
from datetime import timedelta
import random


class Faculty(QuxModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    
    
    @classmethod
    def random_faculty(cls):  
        faker = Faker()
        for _ in range(5):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name  = faker.last_name()
            email =faker.email()

            user = get_user_model().objects.create_user(email=email , username = username ,first_name = first_name ,last_name =last_name)
            Faculty.objects.create(user = user, github = f"https://github.com/{username}" ,is_active = True)
        
      

    def programs(self):
        return Program.objects.none()

    def courses(self):
        """
          Show the number of courses each faculty is teaching
        """
        
        return self.content_set.filter(assignment__isnull=False).distinct().count()
        

    def assignments_graded(self, assignment=None):
        """
        Show the number of assignments graded by each faculty
        """
        if assignment :
            return StudentAssignment.objects.filter(reviewed =self ,assignment = assignment )
        return StudentAssignment.objects.filter(reviewed =self )
    
    def no_assignments(self):
        """
        Show the number of assignments by each faculty
        """
        return Assignment.objects.filter(program__faculty=self).count()


    def content(self, program=None, course=None):
        """
         content of  programs or courses of  faculty.
        """
        contents = self.content_set.all()

        if program and course:
            ans = set()
            for content in contents:
                assignments = content.assignment_set.filter(
                    program=program, course=course
                )
                if assignments:
                    ans.add(content)
            contents = ans
        elif program:
            ans = set()
            for content in contents:
                assignments = content.assignment_set.filter(program=program)
                if assignments:
                    ans.add(content)
            contents = ans
        elif course:
            ans = set()
            for content in contents:
                assignments = content.assignment_set.filter(course=course)
                if assignments:
                    ans.add(content)
            contents = ans

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
        faker = Faker()
        for _ in range(3):          
            name = faker.first_name()
            start = faker.date_time_this_decade(tzinfo=None) + timedelta(days=faker.random_int(min=1, max=365))
            end  = start + timedelta(days=faker.random_int(min=1, max=365))
            Program.objects.create(name = name, start = start,end = end)
        

    def __str__(self):
        return self.name

    def students(self):
        """
        List of students in the program
        """
        return self.student_set.all().count()
    


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    @classmethod
    def random_course(cls):  
        faker = Faker()
        for _ in range(3):          
            name = faker.first_name()            
            Course.objects.create(name = name)
        

    def __str__(self):
        return self.name

    def programs(self):
        return Program.objects.none()

    def students(self):
        return Student.objects.none()

    def content(self):
        return Content.objects.none()

    def assignments(self):
        return Assignment.objects.none()


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class _Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"

    @classmethod
    def random_content(cls):  
        faker = Faker()
        for i in range(28):
            id = int(random.sample(range(2,6), 1)[0])
            repo =  f"https://github.com/{i}"
            Content.objects.create(name = faker.first_name(), faculty = Faculty.objects.get(pk=id) ,repo = repo)
        

class Student(QuxModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    @classmethod
    def random_student(cls):  
        faker = Faker()
        for _ in range(10):
            username = faker.user_name()
            first_name = faker.first_name()
            last_name  = faker.last_name()
            email =faker.email()

            user = get_user_model().objects.create_user(email=email , username = username ,first_name = first_name ,last_name =last_name)
            id = int(random.sample(range(1,3), 1)[0])
            program = Program.objects.get(pk=id)
            Student.objects.create(user = user, github = f"https://github.com/{username}" ,is_active = True ,program = program )
        

    def courses(self):
        return Course.objects.none()

    def assignments(self):
        return Assignment.objects.none()

    def assignments_submitted(self, assignment=None):
        return StudentAssignment.objects.none()

    def assignments_not_submited(self, assignment=None):
        return StudentAssignment.objects.none()

    def assignments_graded(self, assignment=None):
        return StudentAssignment.objects.none()


class Assignment(QuxModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()


    @classmethod
    def random_assignment(cls):  
        faker = Faker()
        for _ in range(5):
          
            rubric = faker.name()
            instructions = faker.last_name()
            pro_id = int(random.sample(range(1,3), 1)[0])
            con_id = int(random.sample(range(1,28), 1)[0])
            program = Program.objects.get(pk=pro_id)
            content = Content.objects.get(pk=con_id )
            course =  Course.objects.get(pk=pro_id)
            due = faker.date_time_between_dates(datetime_start=program.start, datetime_end=program.end, tzinfo=None)
            Assignment.objects.create(due = due, course =course ,content = content ,program = program,instructions =instructions,rubric =rubric )
        

    class Meta:
        unique_together = ["program", "course", "content"]

    def __str__(self):
        return self.content.name

    def students(self):
        return Student.objects.none()

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        return StudentAssignment.objects.none()


class StudentAssignment(QuxModel):
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
        faker = Faker()
        for _ in range(5):
            stud_id = int(random.sample(range(1,10), 1)[0])
            a_id = int(random.sample(range(1,5), 1)[0])
            grade = random.uniform(30, 100)
            assignment = Assignment.objects.get(pk=a_id)
            student = Student.objects.get(pk=stud_id)
            reviewer = Faculty.objects.get(pk=a_id)
            feedback = faker.text()
            pro_id = int(random.sample(range(1,3), 1)[0])       
            program = Program.objects.get(pk=pro_id)      
            submitted = faker.date_time_between_dates(datetime_start=program.start, datetime_end=program.end, tzinfo=None)
            reviewed =  faker.date_time_between_dates(datetime_start=submitted, datetime_end=program.end, tzinfo=None)
            StudentAssignment.objects.create(grade = grade, assignment =assignment ,student = student ,submitted = submitted,
                                      reviewer =reviewer,feedback =feedback,reviewed = reviewed)
        
