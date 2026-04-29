from django.db import models
from Students.models import Student
from Admins.models import Class,Subject,AcademicSession,Term,School

#Model for Students Results Summary
class ResultSummary(models.Model):
	Student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
	TotalScore=models.CharField(max_length=100, blank=True,null=True , default="-")
	Totalnumber=models.CharField(max_length=100, blank=True,null=True , default="-")
	Average=models.CharField(max_length=100, blank=True,null=True , default="-")
	Position=models.CharField(max_length=100, blank=True,null=True , default="-")
	Remark=models.CharField(max_length=100, blank=True,null=True , default="-")
	Term=models.ForeignKey(Term,on_delete=models.CASCADE,blank=True,null=True)
	AcademicSession=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,blank=True,null=True)
	published = models.BooleanField(default=False)


	def __str__(self):
		term = self.Term.term if self.Term else "No Term"
		session = self.AcademicSession.session if self.AcademicSession else "No Session"
		return str(self.Student_name.firstname+"-"+self.Student_name.student_class.Class+"-"+term+"-"+session)

#Model for Students Subject Results
class SubjectResult(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	Subject= models.ForeignKey(Subject,on_delete=models.CASCADE)
	FirstTest= models.CharField(max_length=100, blank=True,null=True , default="-")
	FirstAss= models.CharField(max_length=100, blank=True,null=True , default="-")
	MidTermTest= models.CharField(max_length=100, blank=True,null=True , default="-")
	Project= models.CharField(max_length=100, blank=True,null=True , default="-")
	SecondAss= models.CharField(max_length=100, blank=True,null=True , default="-")
	SecondTest= models.CharField(max_length=100, blank=True,null=True , default="-")
	CA= models.CharField(max_length=100, blank=True,null=True , default="-")
	Exam= models.CharField(max_length=100, blank=True,null=True , default="-")
	Total= models.CharField(max_length=100, blank=True,null=True , default="-")
	Grade=models.CharField(max_length=100, blank=True,null=True , default="-")
	SubjectPosition=models.CharField(max_length=100, blank=True,null=True , default="-")
	Remark=models.CharField(max_length= 100, blank=True,null=True , default="-")
	Term=models.ForeignKey(Term,on_delete=models.CASCADE,blank=True,null=True)
	AcademicSession=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,blank=True,null=True)
	student_class=models.ForeignKey(Class,on_delete=models.CASCADE, blank=True,null=True)
	student_school=models.ForeignKey(School,on_delete=models.CASCADE, blank=True,null=True)
	is_offering = models.BooleanField(default=True)
	published = models.BooleanField(default=False)


	def __str__(self):
		term = self.Term.term if self.Term else "No Term"
		return str(self.student.firstname + " - " + self.Subject.subject_name+' '+ term)

	


# Model for Annual Students Results Summary
class AnnualResultSummary(models.Model):
	Student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
	TotalScore=models.CharField(max_length=100, blank=True,null=True , default="-")
	Totalnumber=models.CharField(max_length=100, blank=True,null=True , default="-")
	Average=models.CharField(max_length=100, blank=True,null=True , default="-")
	Position=models.CharField(max_length=100, blank=True,null=True , default="-")
	PrincipalVerdict=models.CharField(max_length=100, blank=True,null=True , default="-")
	AcademicSession=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,blank=True,null=True)
	published = models.BooleanField(default=False)

	def __str__(self):
		session = self.AcademicSession.session if self.AcademicSession else "No Session"
		return str(self.Student_name.firstname +"-"+ self.Student_name.student_class.Class + " "+ session)

# Model for Annual Students Subject Results
class AnnualSubjectResult(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	Subject= models.ForeignKey(Subject,on_delete=models.CASCADE)
	FirstTermTotal= models.CharField(max_length=100, blank=True,null=True,default="-")
	SecondTermTotal= models.CharField(max_length=100, blank=True,null=True,default="-")
	ThirdTermTotal= models.CharField(max_length=100, blank=True,null=True,default="-")
	Total= models.CharField(max_length=100, blank=True,null=True,default="-")
	Average= models.CharField(max_length=100, blank=True,null=True,default="-")
	Grade=models.CharField(max_length=100, blank=True,null=True,default="-")
	SubjectPosition=models.CharField(max_length=100, blank=True,null=True,default="-")
	Remark=models.CharField(max_length= 100, blank=True,null=True, default="-")
	AcademicSession=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,blank=True,null=True)
	is_offering = models.BooleanField(default=True)
	published = models.BooleanField(default=False)
	
	def __str__(self):
		session = self.AcademicSession.session if self.AcademicSession else "No Session"
		return str(self.student.firstname +"-"+ self.Subject.subject_name+" "+ session)