from django.urls import path
from . import views
from .views import incoming_call


urlpatterns = [
    path('', views.landing, name='landing'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),
    path('api/fari/chat/', views.fari_chat, name='fari_chat'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("incoming-call/", incoming_call),
    path('process-intent/', views.process_intent),
    path('choose-slot/', views.choose_slot),
    path('confirm-booking/', views.confirm_booking),
]


