from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('generate-card/<str:pk>/',views.generate_card,name='generate_card'),
    path('full-details/',views.full_details,name='full_details')
]