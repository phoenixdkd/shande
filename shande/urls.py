"""shande URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from super import urls as superurls
from ops import urls as opsurls
from sale import urls as saleurls
from customer import urls as customerurls
from teacher import urls as teacherurls
from bursar import urls as bursarurls
from wxqq import urls as wxqqurls
from trade import urls as tradeurls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # app super [default]
    url(r'', include(superurls, namespace="super")),

    # app ops
    url(r'^ops/', include(opsurls, namespace="ops")),

    # app sale
    url(r'^sale/', include(saleurls, namespace="sale")),

    # app customer
    url(r'^customer/', include(customerurls, namespace="customer")),

    # app teacher
    url(r'^teacher/', include(teacherurls, namespace="teacher")),

    # app bursar
    url(r'^bursar/', include(bursarurls, namespace="bursar")),

    # app wxqq
    url(r'^wxqq/', include(wxqqurls, namespace="wxqq")),

    # app trade
    url(r'^trade/', include(tradeurls, namespace="trade")),
]
