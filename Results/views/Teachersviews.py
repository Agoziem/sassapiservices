from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from Admins.models import *
from Students.models import Student, StudentClassEnrollment


# get all results for a subject in a term and session
@api_view(['POST'])
def getResults(request):
    data = request.data
    try:
        term = Term.objects.get(id=data['term_id'])
        session = AcademicSession.objects.get(id=data['session_id'])
        school = School.objects.get(id=data['school_id'])
        student_class = Class.objects.get(id=data['class_id'])
        subject = Subject.objects.get(id=data['subject_id'])
        studentsinclass = StudentClassEnrollment.objects.filter(academic_session=session,student_class=student_class)
        studentsubjectResults = []
        for student in studentsinclass:
            studentresult,created = SubjectResult.objects.get_or_create(student=student.student,Subject=subject,Term=term,AcademicSession=session,student_class=student_class,student_school=school)
            studentsubjectResults.append({
                'id': studentresult.id,
                'firstname': studentresult.student.firstname,
                'surname': studentresult.student.surname,
                'middlename': studentresult.student.othername,
                'studentID': studentresult.student.student_id,
                'subject': studentresult.Subject.subject_name,
                'is_offering': studentresult.is_offering,
                'FirstTest': studentresult.FirstTest,
                'FirstAss': studentresult.FirstAss,
                'MidTermTest': studentresult.MidTermTest,
                "Project":studentresult.Project,
                'SecondAss': studentresult.SecondAss,
                'SecondTest': studentresult.SecondTest,
                'CA':studentresult.CA,
                'Exam': studentresult.Exam,
                'Total': studentresult.Total,
                'Grade': studentresult.Grade,
                'SubjectPosition': studentresult.SubjectPosition,
                'Remark': studentresult.Remark,
                'published': studentresult.published
            })
        return Response(studentsubjectResults, status=status.HTTP_200_OK)
    except:
        studentsubjectResults = []
        return Response(studentsubjectResults, status=status.HTTP_200_OK)

# api for getting a single student result
@api_view(['GET'])
def getResult(request, result_id):
    try:
        result = SubjectResult.objects.get(id=result_id)
        serializer = SubjectResultSerializer(result, many=False)
        return Response(serializer.data)
    except SubjectResult.DoesNotExist:
        return Response('Result Record does not exist')

# update student result 
@api_view(['PUT'])
def updateResult(request, result_id):
    data = request.data
    try:
        result = SubjectResult.objects.get(id=result_id)
        fields_to_update = ['CA', 'Exam', 'is_offering']
        for field in fields_to_update:
            if field in data:
                setattr(result, field, data[field])
        result.save()
        return Response(f"{result.student.firstname}'s Subject Result Record Updated Successfully",status=status.HTTP_200_OK)
    except SubjectResult.DoesNotExist:
        return Response('Result Record does not exist')



# post and update all the student subject results with Total, Grade, Subject Position and Remark
@api_view(['PUT'])
def postResults(request):
    data = request.data
    for studentrecord in data:
        try:
            studentresult = SubjectResult.objects.get(id=studentrecord['id'])
        
            fields_to_update = ['FirstTest','FirstAss','MidTermTest',
                                'Project','SecondAss','SecondTest',"CA",
                                'Exam','is_offering','Total','Grade',
                                'SubjectPosition','Remark']
            for field in fields_to_update:
                if field in studentrecord:
                    setattr(studentresult, field, studentrecord[field])

            studentresult.published = True
            studentresult.save()
            
        except Exception as e:
            print(str(e))
            pass
    return Response('Results Published Successfully')


# view to unpublish all the Student Results
@api_view(['PUT'])
def unpublishResults(request):
    data = request.data
    for studentrecord in data:
        try:
            studentresult = SubjectResult.objects.get(id=studentrecord['id'])
            studentresult.published = False
            studentresult.save()
        except Exception as e:
            print(str(e))
            pass
    return Response('Results Unpublished Successfully')


# //////////////////////////////////////////// Teachers Annual Results ////////////////////////////////////////////

# view for creating & getting all students annual result for a subject
@api_view(['POST'])
def getAnnualResults(request):
    data = request.data
    try:
        session = AcademicSession.objects.get(id=data['session_id'])
        school = School.objects.get(id=data['school_id'])
        student_class = Class.objects.get(id=data['class_id'])
        subjectannual = Subject.objects.get(id=data['subject_id'])
        studentsinclass = StudentClassEnrollment.objects.filter(academic_session=session,student_class=student_class)
        studentssubjectAnnualResult = []
        for student in studentsinclass: 
            termlystudentresults = SubjectResult.objects.filter(student=student.student,Subject=subjectannual,AcademicSession=session)
            for result in termlystudentresults:
                if result.Term.term == '1st Term':
                    firsttermresult = result.Total
                elif result.Term.term == '2nd Term':
                    secondtermresult = result.Total
                else:
                    thirdtermresult = result.Total
            annualstudentresult,created = AnnualSubjectResult.objects.get_or_create(student=student,Subject=subjectannual,AcademicSession=session)
            studentssubjectAnnualResult.append({
                'id': annualstudentresult.id,
                'firstname': annualstudentresult.student.firstname,
                'surname': annualstudentresult.student.surname,
                'middlename': annualstudentresult.student.othername,
                'studentID': annualstudentresult.student.student_id,
                'FirstTermTotal':  firsttermresult,
                'SecondTermTotal': secondtermresult,
                'ThirdTermTotal': thirdtermresult,
                'Total': annualstudentresult.Total,
                'Average': annualstudentresult.Average,
                'Grade': annualstudentresult.Grade,
                'SubjectPosition': annualstudentresult.SubjectPosition,
                'Remark': annualstudentresult.Remark,
                'is_offering': annualstudentresult.is_offering,
                'published': annualstudentresult.published
            })
        return Response(studentssubjectAnnualResult, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        studentssubjectAnnualResult = []
        return Response(studentssubjectAnnualResult, status=status.HTTP_200_OK)

# api view for getting a single student annual result
@api_view(['GET'])
def getAnnualResult(request, result_id):
    try:
        result = AnnualSubjectResult.objects.get(id=result_id)
        serializer = AnnualSubjectResultSerializer(result, many=False)
        return Response(serializer.data)
    except AnnualSubjectResult.DoesNotExist:
        return Response('Annual Result Record does not exist')
    
# view for updating all Students Annual Result for a Subject by the Teacher
@api_view(['PUT'])
def updateAnnualResult(request, result_id):
    data = request.data
    try:
        studentresult = AnnualSubjectResult.objects.get(id=result_id)
        fields_to_update = ['FirstTermTotal','SecondTermTotal','ThirdTermTotal','is_offering']
        for field in fields_to_update:
            if field in data:
                setattr(studentresult, field, data[field])
        studentresult.save()
        return Response('Annual Result Updated Successfully')
    except AnnualSubjectResult.DoesNotExist:
        return Response('Annual Result Record does not exist')

# view for submitting all Students Annual Result for a Subject by the Teacher
@api_view(['PUT'])
def postAnnualResults(request):
    data = request.data
    for studentannualrecord in data:
        try:
            studentresult = AnnualSubjectResult.objects.get(id=studentannualrecord['id'])
            fields_to_update = ['FirstTermTotal','SecondTermTotal','ThirdTermTotal','Total','Average','Grade','SubjectPosition','Remark']
            for field in fields_to_update:
                if field in studentannualrecord:
                    setattr(studentresult, field, studentannualrecord[field])
            
            studentresult.published = True
            studentresult.save()
        except Exception as e:
            print(str(e))
            pass
    return Response('Annual Results Published Successfully')

# view to unpublish all the Student Annual Results
@api_view(['PUT'])
def unpublishAnnualResults(request):
    data = request.data
    for studentrecord in data:
        try:
            studentresult = AnnualSubjectResult.objects.get(id=studentrecord['id'])
            studentresult.published = False
            studentresult.save()
        except Exception as e:
            print(str(e))
            pass
    return Response('Annual Results Unpublished Successfully')