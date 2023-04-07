from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app1.views import (
    RegisterView,
    ContentListView,
    ContentCreateView,
    ContentDetailView,
    ContentSearchView,
    ContentUpdateView,
    ContentDeleteView
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/content/', ContentListView.as_view(), name='content_list'),
    path('api/content/create/', ContentCreateView.as_view(), name='content_create'),
    path('api/content/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),
    path('api/search/',ContentSearchView.as_view()),
    path('api/content/<int:pk>/update/', ContentUpdateView.as_view(), name='content_update'),
    path('api/content/<int:pk>/delete/', ContentDeleteView.as_view(), name='content_delete'),
]
