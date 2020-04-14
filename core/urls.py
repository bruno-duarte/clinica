from django.urls import path, include
from .views import IndexView, AboutView, ContactView, ElementsView, NewsView, \
	ServicesView, SignupView, ProfileView, PrescriptionsView, MedicalRecordsView, \
    ChangePasswordView, BookingView, BookingResultsView


from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


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

	# Login and Logout
    path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='commons/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Change Password
    path(
        'change-password/',
        ChangePasswordView.as_view(
            template_name='commons/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),

    # Forget Password
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