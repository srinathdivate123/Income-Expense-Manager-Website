from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index, name='nexpenses'),
    path('add_expense', views.add_expense, name='nadd_expense'),
    path('edit_expense/<int:id>', views.expense_edit, name='nexpense_edit'),
    path('delete_expense/<int:id>', views.delete_expense, name='nexpense_delete'),
    path('search_expenses', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('expense_category_summary', views.expense_category_summary, name="expense_category_summary"),
    path('e_stats', views.stats_view, name="e_stats"),

    
]
