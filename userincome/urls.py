from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index, name='nincome'),
    path('add_income', views.add_income, name='nadd_income'),
    path('edit_income/<int:id>', views.income_edit, name='nincome_edit'),
    path('delete_income/<int:id>', views.delete_income, name='nincome_delete'),
    path('search_income', csrf_exempt(views.search_income), name='nsearch_income'),
    path('i_stats', views.stats_view, name="i_stats"),
    path('income_source_summary', views.income_source_summary, name="income_source_summary"),

    
]
