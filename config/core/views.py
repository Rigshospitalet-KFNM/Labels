from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, 'core/main_page.html')