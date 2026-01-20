from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("studentsapi/", include("Students.urls")),
    path("teachersapi/", include("Teachers.urls")),
    path("adminsapi/", include("Admins.urls")),
    path("resultapi/", include("Results.urls")),
    path("chatroomapi/", include("ChatSystem.urls")),
    path("Authentication/", include("Authentication.urls")),
]


if settings.DEBUG_ENV:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header='St Andrews Backend'
admin.site.index_title='Site Administration'
