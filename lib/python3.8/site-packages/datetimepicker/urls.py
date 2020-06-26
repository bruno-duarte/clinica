from django.conf.urls import url

from .views import JSTemplateView


urlpatterns = [url(r'^loader.js',
               JSTemplateView.as_view(),
               name='datetimepicker-loader')]
