from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user.views import RegisterView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/posts/', include('post.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/register/', RegisterView.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
