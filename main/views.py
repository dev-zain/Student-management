from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def generate_card(request):
    return render(request,'main/generate_card.html')

def full_details(request):
    return render(request,'main/full_details.html')