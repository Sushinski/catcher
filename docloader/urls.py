__author__ = 'mac'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'docloader.views.upload_view', name='upload_view'),
                       url(r'^result/$', 'docloader.views.upload_result_view', name='upload_result_view'),
                       url(r'^result/parse_upload/$', 'docloader.views.parse_uploaded_file', name='parse_uploaded_view'),
                       url(r'^preview/$', 'docloader.views.preview_uploaded_file', name='preview_uploaded_file'),
                       )