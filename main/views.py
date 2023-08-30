from django.shortcuts import redirect, render
from .models import Student
from .forms import StudentForm
from django.db.models import Q
import cv2
import numpy as np
from pyzbar.pyzbar import decode
# Create your views here.

def home(request):
    search_query = request.GET.get('search')
    students = Student.objects.all()

    if search_query:
        students = students.filter(
            Q(student_name__icontains=search_query) | Q(department__icontains=search_query)
        )

    context = {
        'students': students,
    }
    return render(request, 'main/home.html', context)


def generate_card(request,pk):
    student = Student.objects.get(id=pk)

    context = {
        'student' : student,
    }
    return render(request,'main/generate_card.html',context)

def full_details(request,pk):
    student = Student.objects.get(id=pk)

    context = {
        'student' : student,
    }
    return render(request,'main/full_details.html',context)

def update_student(request, pk):
    student = Student.objects.get(id=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
    }

    return render(request, 'main/update_student.html', context)

def delete_student(request,pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('home')
    
    context = {
        'student' : student,
    }
    return render(request,'main/delete_student.html',context)


def add_user(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()

    context = {
        'form': form,
    }

    return render(request, 'main/add_user.html', context)

    
def identify(request):
    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        while True:
            success, img = cap.read()

            for qrcode in decode(img):
                myData = qrcode.data.decode('utf-8')

                try:
                    student = Student.objects.get(id_card_number=myData)
                    myOutput = 'Authorized: ' 
                    myColor = (0, 255, 0)

                    # Show student information on the camera screen
                    cv2.putText(img, student.student_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, myColor, 2)
                    cv2.putText(img, student.department, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, myColor, 2)
                    cv2.putText(img, student.roll_no, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, myColor, 2)
                except Student.DoesNotExist:
                    myOutput = 'Unauthorized Access Denied'
                    myColor = (0, 0, 255)

                pts = np.array([qrcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, myColor, 5)
                pts2 = qrcode.rect
                cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, myColor, 2)

            cv2.imshow('Result', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print("An error occurred:", str(e))


