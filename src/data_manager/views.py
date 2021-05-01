from django.shortcuts import render

# Create your views here.
def add_data_main_view(request):
    return render(request, "add_data/add_data.html")