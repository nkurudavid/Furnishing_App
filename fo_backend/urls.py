from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# THE FOLLOWING FUNCTION WILL HELP US TO HANDLE THE UNAVAILABLE LINK OR WEB PAGE
handler404 = "main.views.handle_not_found"


# Configure Admin Title
admin.site.site_header = "Furnishing Order System"
admin.site.index_title = "Management"
admin.site.site_title = "Control Panel"
admin.site.index_template = 'admin/admin_index.html'