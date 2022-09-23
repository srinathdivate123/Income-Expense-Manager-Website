from django.urls import path
from . import views
urlpatterns = [
    path('others_summary', views.ViewOthersSummary, name='others_summary')
]
