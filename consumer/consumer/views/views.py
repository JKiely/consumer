from django.http import HttpResponse


def index(request):
    return HttpResponse("Consumer index page")
