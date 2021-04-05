from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('messenger/', include('messenger.urls')),
    path('account/', include('accounts.urls')),
    path('anonymous/', include('anonymous.urls')),
    path('blog/', include('blog.urls')),
    path('search/', include('search.urls')),
    path('', include('shortener.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
