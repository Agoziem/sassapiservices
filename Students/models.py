from django.db import models
import random
from Admins.models import AcademicSession, Class,School
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# model for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=2,blank=True,null=True)
    firstname=models.CharField(max_length=100, blank=True, default="None",null=True)
    surname=models.CharField(max_length=100, blank=True, default="None",null=True)
    othername=models.CharField(max_length=100, blank=True, default="None",null=True)
    sex=models.CharField(max_length=100, blank=True,null=True)
    student_id=models.CharField(max_length=100, blank=True,null=True)
    student_pin=models.CharField(max_length=100, blank=True,null=True)
    role = models.CharField(max_length=100, blank=True, default="Student")
    headshot=models.ImageField(upload_to="assets/Students",blank=True,null=True)
    student_school=models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f"{self.surname} {self.firstname} - {self.student_id}"

# 

    # save method to generate student_id and student_pin
    def save(self, *args, **kwargs):
        if not self.pk: 
            attempts = 0
            while attempts < 5:  # Limit the number of attempts to avoid infinite loop
                random_pin = str(random.randint(1000, 9999))
                random_14_digit = str(random.randint(10**13, 10**14 - 1))
                student_id = f"SASS/{random_pin}"
                if not Student.objects.filter(student_id=student_id, student_pin=random_14_digit).exists():
                    self.student_id = student_id
                    self.student_pin = random_14_digit
                    break
                attempts += 1
            else:
                raise ValueError("Unable to generate a unique student ID")
            username = f"@{str(self.surname)}{str(self.firstname)}{random_pin}"
            user = User.objects.create_user(username=username, password=self.student_id)
            self.user = user
            Token.objects.create(user=user)
        super().save(*args, **kwargs)

    # delete the user when the Student is deleted
    def delete(self, *args, **kwargs):
        if self.user:
            user = User.objects.filter(id=self.user.id).first()
            if user:
                user.delete()
        super().delete(*args, **kwargs)
		
    # return the URL of the student's photo
    @property
    def imageURL(self):
        try:
            url= self.student_Photo.url
        except:
            url=''
        return url
    
# New Model: StudentClassEnrollment
class StudentClassEnrollment(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.firstname} {self.student.surname} - {self.student_class.Class} in {self.academic_session.session}"