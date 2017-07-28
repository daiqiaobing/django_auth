from django.conf.urls import include, url
from django.contrib import admin

handler404 = 'common.page.page_not_found'
handler403 = 'common.page.page_not_permission'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.blog_urls')),
 ]


