from django.shortcuts import render
from .models import Exam
def exams(request):
    if True:
        exam = Exam.objects.create(
            name = 'dd'
        )
    #exams = ['one' , 'two' , 'three']
    ##for exam in exams:
        #answer = ['A','B', 'C' , 'D']
    context = {'exams' : exam }
    return render(request , 'exams.html' , context)

