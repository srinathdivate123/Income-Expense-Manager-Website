from django.shortcuts import render

# Create your views here.
def ViewOthersSummary(request):
    return render (request, 'others/viewothers.html')
