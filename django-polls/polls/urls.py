from django.conf.urls import url
from . import views

#pay attention to the name parameter to url() - this gets used instead of the hardcoded
#url address in order to be able to change the url address later on

#app_name means that the template tag {% url %} does not confuse any other views that might be named 'detail'
#in the template, it specificallt tells the tag to look up 'polls:detail'
app_name = 'polls'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name = "index"),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
	url(r'^(?P<pk>[0-9]+)/result/$', views.ResultsView.as_view(), name = 'result'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	
]
