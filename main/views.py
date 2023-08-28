from django.shortcuts import render
from .models import Student
# Create your views here.

def home(request):
    students = Student.objects.all()

    context = {
        'students' : students,
    }
    return render(request, 'main/home.html',context)

def generate_card(request,pk):
    student = Student.objects.get(id=pk)

    context = {
        'student' : student,
    }
    return render(request,'main/generate_card.html',context)

def full_details(request):
    return render(request,'main/full_details.html')