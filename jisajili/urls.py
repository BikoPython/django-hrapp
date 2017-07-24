from django.conf.urls import url
from .views import home,show_candidates,CreateApplication,SingleApplicant

urlpatterns =[
   url(r'^$',show_candidates,name='candidates'),
   url(r'^apply/$',CreateApplication.as_view(),name='apply'),
   #url(r'^candidates/$',show_candidates,name='candidates'),
   url(r'^applicant/(?P<id>\d+)/$',SingleApplicant.as_view(),name='singleApplicant'),

]
