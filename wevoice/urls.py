from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

# Examples:
# url(r'^$', 'wevoice.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^', include('choices.urls')),
    url(r'^choices/', include('choices.urls')),
    url(r'^admin/', include(admin.site.urls)),
]