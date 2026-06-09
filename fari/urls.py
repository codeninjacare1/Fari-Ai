from django.urls import path
from . import views
from .views import incoming_call


urlpatterns = [
    path('', views.landing, name='landing'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),
    path('api/fari/chat/', views.fari_chat, name='fari_chat'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('process-intent/', views.process_intent),
    path('choose-slot/', views.choose_slot),
    path('confirm-booking/', views.confirm_booking),
    path('incoming-call/', views.incoming_call),
    path('recording-callback/', views.recording_callback),

    path('save-name/', views.save_name),
    path('save-reason/', views.save_reason),
    path('save-number/', views.save_number),
    path('save-message/', views.save_message),
]




