"""atlantos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^', include('djcore.djcore.core.urls')),
    #url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^admin/', admin.site.urls),

    url(r'^users/', include('djcore.djcore.users.urls', namespace='users')),
    url(r'^groups/', include('djcore.djcore.groups.urls', namespace='groups')),
    url(r'^forcastattributes/', include('padoa.forecastattributes.urls', namespace='forcastattributes')),
    url(r'^maps/', include('padoa.thredds.urls', namespace='thredds')),
    url(r'^places/', include('padoa.places.urls', namespace='places')),
    ## todo MAPPARE TUTTI GLI URL NUOVI
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
