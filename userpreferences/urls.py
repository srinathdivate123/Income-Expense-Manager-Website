from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', views.index , name="npreferences"),
    path('show_others', views.SharePreference_View , name="nshow_others"),
    path('income_source_summary', views.income_source_summary, name="income_source_summary"),
    path('expense_category_summary', views.expense_category_summary, name="expense_category_summary"),
    path('view_others_summary', views.ViewOthersSummary , name="nviewothers"),
    path('activate/<uidb64>/<uidb32>', views.VerificationView , name="nVerificationView"),
]