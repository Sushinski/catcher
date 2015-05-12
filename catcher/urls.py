from django.conf.urls import include, url
from django.contrib import admin
from docloader import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'catcher.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^docloader/', include('docloader.urls')),
]
