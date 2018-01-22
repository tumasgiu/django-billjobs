from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^generate_pdf/(?P<bill_id>\d+)$', views.generate_pdf,
            name='generate-pdf'),
        url(r'^$', views.home, name='home'),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^bills/$', views.bills, name='bills'),
        url(r'^bills/new/$', views.create_bill, name='create_bill'),
        url(r'^onboarding/$', views.onboarding, name='onboarding'),
        url(r'^directory/$', views.directory, name='directory'),
        url(r'^signup-success/$', views.signup_success,
            name='billjobs_signup_success')
        ]
