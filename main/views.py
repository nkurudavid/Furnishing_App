from django.shortcuts import render

# Create your views here.

# Create your views here.
def handle_not_found(request, exception):
    return render(request, 'page_404/404.html')



def home(request):
    return render(request, 'main/home.html');
