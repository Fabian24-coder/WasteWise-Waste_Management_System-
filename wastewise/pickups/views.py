from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import pickup_request

# Create your views here.

def pickup_request_views(request):
    # return HttpResponse("This is the pickup request view.")
    pickup_requests = pickup_request.objects.all()
    context = {
        'pickup_requests': pickup_requests
    }
    return render(request, 'pickups/pickup_requests.html', context)
    