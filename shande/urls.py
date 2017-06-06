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
from spot import urls as spoturls
from stock import urls as stockurls
from analyst import urls as analysturls
from shande.settings import STATIC_ROOT
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

    # app spot
    url(r'^spot/', include(spoturls, namespace="spot")),

    # app stock
    url(r'^stock/', include(stockurls, namespace="stock")),

    # app analyst
    url(r'^analyst/', include(analysturls, namespace="analyst")),
]
#
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.UPLOAD_ROOT)
#     urlpatterns.append(url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)