'''
Created on Aug 17, 2018

@author: SINHPN
'''
from django.conf.urls import url
from . import views

app_name = 'testapp'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add-question/$', views.AddQuestionView.as_view(), name='add-question'), 
    url(r'^detail/(?P<question_id>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/$', views.VoteView.as_view(), name='vote'),
    url(r'^(?P<question_id>[0-9]+)/add-choice/$', views.AddChoiceView.as_view(), name='add-choice'),
    url(r'^(?P<question_id>[0-9]+)/delete-view/$', views.DeleteQuestion.as_view(), name='delete-view'),
]