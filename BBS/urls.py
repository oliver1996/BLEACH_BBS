from django.conf.urls import patterns, include, url
from django.contrib import admin
import mybbs.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BBS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include(mybbs.urls)),
)
