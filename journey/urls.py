from django.urls import path
from . import views

urlpatterns = [
    path('', views.JourneyCreateAPIView.as_view()),
    path('generate/', views.JourneyGenerateAPIView.as_view()),
    path('save/', views.JourneyCreateAPIView.as_view()),
    path('<int:pk>/update', views.JourneyUpdateAPIView.as_view())
    # path('save/', views.JourneySaveAPIView.as_view())
]
