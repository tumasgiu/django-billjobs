from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
            name='generate-pdf'),
        url(r'^onboarding/$', views.onboarding, name='onboarding'),
        url(r'^signup-success/$', views.signup_success,
            name='billjobs_signup_success')
        ]
