from django.urls import path
from .views import IndexView, AboutView, ContactView, ElementsView, NewsView, ServicesView


urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('about', AboutView.as_view(), name='about'),
	path('contact', ContactView.as_view(), name='contact'),
	path('elements', ElementsView.as_view(), name='elements'),
	path('news', NewsView.as_view(), name='news'),
	path('services', ServicesView.as_view(), name='services'),
]