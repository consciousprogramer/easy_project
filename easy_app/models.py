from django.db import models
from django.contrib.postgres.fields import ArrayField,JSONField
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

class students_registration_number_database(models.Model):
    registeration_numbers = ArrayField(models.PositiveIntegerField())

class teachers_id_numbers_database(models.Model):
    id_numbers = ArrayField(models.PositiveIntegerField())

class subject(models.Model):
    subject_name = models.CharField(max_length = 150)
    subject_code = models.CharField(max_length = 6)
    started = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return f"{self.subject_name({self.subject_code})}"

class assignment(models.Model):
    subject = models.ManyToManyField(subject,related_name = "assignments")

class students_class(models.Model):
    class_number = models.PositiveIntegerField()
    assignments = models.ForeignKey(assignment,on_delete = models.DO_NOTHING)
    def __str__(self):
        return f"class {self.class_number}"

class class_section(models.Model):
    section_name = models.CharField(max_length = 1)
    section_of_class = models.ForeignKey(students_class,on_delete = models.CASCADE)
    section_class_teacher = models.OneToOneField("class_teacher",on_delete = models.SET_NULL,null = True,related_name = "class_teacher_of")

    def __str__(self):
        return f"section {self.section_of_class.class_number} {self.section_name}"

class student(models.Model):
    user = models.OneToOneField(User,on_delete = models.PROTECT)
    name = models.CharField(max_length = 64)
    students_class = models.ForeignKey(students_class,on_delete = models.PROTECT)
    class_section = models.ForeignKey(class_section,on_delete = models.PROTECT)

    def __str__(self):
        return self.name


class teacher(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length = 64)
    students = models.ManyToManyField(student, related_name = "teachers")

    def __str__(self):
        return self.name

class class_teacher(models.Model):
    teacher = models.OneToOneField(teacher,on_delete = models.CASCADE)
    section = models.OneToOneField(class_section,on_delete = models.SET_NULL,null= True)

    def __str__(self):
        return f"class teacher of{self.section.section_of_class.class_number}"
