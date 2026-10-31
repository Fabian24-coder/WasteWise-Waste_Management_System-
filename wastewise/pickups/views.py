from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import pickup_request
from .forms import CreatePickUpRequestForm, Update_pickup_requestForm
from django.core.paginator import Paginator

# Create your views here.

def pickup_request_views(request):
    # return HttpResponse("This is the pickup request view.")
    
    pickup_requests = pickup_request.objects.all().order_by('-id')
    paginate = Paginator(pickup_requests, 6)
    page_number = request.GET.get("page")
    page_obj = paginate.get_page(page_number)
    context = {
        'pickup_requests': pickup_requests,
        'page_obj': page_obj
    }
    return render(request, 'pickups/pickup_requests.html', context)


def createpickUp_request_Views(request):
    if request.method == "POST":
        make_pickup_request = CreatePickUpRequestForm(request.POST)
        if make_pickup_request.is_valid():
            make_pickup_request.save()
            return redirect("pickup_request_views")
    else:
        make_pickup_request = CreatePickUpRequestForm()

    context = {"make_pickup_request": make_pickup_request} #context can be renamed anything
    return render(request, "pickups/make_pickup_request.html",context)

def update_pickup_requests(request,pickup_request_id):
    get_pickup_request = pickup_request.objects.get(id=pickup_request_id)
    if request.method == "POST":
        update_pickup_request = Update_pickup_requestForm(request.POST, instance=get_pickup_request)
        if update_pickup_request.is_valid():
            update_pickup_request.save()
            return redirect("pickup_request_views")
    else:
        update_pickup_request = Update_pickup_requestForm(instance=get_pickup_request)

    context = {"update_pickup_request": update_pickup_request} #context can be renamed anything
    return render(request, "pickups/update_pickup_request.html",context)