from django.conf.urls import include, url
from analyst import views
urlpatterns = [
    url(r'^analystManage$', views.analystManage, name='analystManage'),
    url(r'^queryAnalyst$', views.queryAnalyst, name='queryAnalyst'),
    url(r'^addAnalyst$', views.addAnalyst, name='addAnalyst'),
    url(r'^addAnalystGroup$', views.addAnalystGroup, name='addAnalystGroup'),
    url(r'^delAnalyst$', views.delAnalyst, name='delAnalyst'),
]