from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import (
    IndexView, AboutView, ContactView, ElementsView, NewsView, 
    ServicesView, SignupView, ProfileView, PrescriptionsView, MedicalRecordsView, 
    ChangePasswordView, BookingView, BookingResultsView, CancelConsultaView, 
    UpdateConsultaView, AppointmentsView, AllAppointmentsView, ReportView, 
    RemoveDataView, NotificationView, ConfirmView, PatientView, UserView,
    DeleteView
)


urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('about', AboutView.as_view(), name='about'),
	path('contact', ContactView.as_view(), name='contact'),
	path('elements', ElementsView.as_view(), name='elements'),
	path('news', NewsView.as_view(), name='news'),
	path('services', ServicesView.as_view(), name='services'),
	path('signup/', SignupView.as_view(), name='signup'),
	path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('prescriptions/<int:pk>/', PrescriptionsView.as_view(), name='prescriptions'),
    path('medical-records/<int:pk>/', MedicalRecordsView.as_view(), name='medical-records'),
    path('booking/<int:pk>/', BookingView.as_view(), name='booking'),
    path('booking-results/<int:pk>/', BookingResultsView.as_view(), name='booking-results'),
    path('cancel/<int:pk>', CancelConsultaView.as_view(), name='cancel'),
    path('today-appointments/<int:pk>', AppointmentsView.as_view(), name='today-appointments'),
    path('update/<int:pk>', UpdateConsultaView.as_view(), name='update'),
    path('appointments/<int:pk>', AllAppointmentsView.as_view(), name='appointments'),
    path('report/<int:pk>', ReportView.as_view(), name='report'),
    path('remove/<int:pk>', RemoveDataView.as_view(), name='remove'),
    path('notification/<int:pk>', NotificationView.as_view(), name='notification'),
    path('confirm/<int:pk>', ConfirmView.as_view(), name='confirm'),
    path('patients/<int:pk>', PatientView.as_view(), name='patients'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete'),
    path('user', UserView.as_view(), name='user'),
    
    path('auth/login', auth_views.LoginView.as_view(redirect_authenticated_user=True, 
                                                template_name='commons/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path(
        'change-password/',
        ChangePasswordView.as_view(
            template_name='commons/change-password.html',
            success_url = reverse_lazy('user')
        ),
        name='change_password'
    ),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]