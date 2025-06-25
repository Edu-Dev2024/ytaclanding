from django.shortcuts import render

def default_landing_view(request):
    return render(request, 'adminhub/index.html')  # Note the namespace