"""test_next_level URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Next Level Test Task API",
      default_version='v1',
   ),
   public=True,
)

urlpatterns = [
    path('openapi<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('admin/', admin.site.urls),
    path('notebook/', include('notebook.urls'))
]
