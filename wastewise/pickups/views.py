from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import pickup_request
from .forms import CreatePickUpRequestForm, Update_pickup_requestForm
from django.core.paginator import Paginator

# Create your views here.

def pickup_request_views(request):
    pickup_requests = pickup_request.objects.all().order_by('-id')

    p = Paginator(pickup_requests,5)
    page_num = request.GET.get('page',2)
    page = p.get_page(page_num)
   
    context = {
        'pickup_requests': pickup_requests,
        'page': page
    }
    return render(request, 'pickups/display_pickup_requests.html', context)

def place_pickUp_request_Views(request):
    if request.method == "POST":
        make_pickup_request = CreatePickUpRequestForm(request.POST)
        if make_pickup_request.is_valid():
            make_pickup_request.save()
            return redirect("pickups:display_pickup_requests")
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
            return redirect("pickups:display_pickup_requests")
    else:
        update_pickup_request = Update_pickup_requestForm(instance=get_pickup_request)

    context = {"update_pickup_request": update_pickup_request} #context can be renamed anything
    return render(request, "pickups/update_pickup_request.html",context)

def delete_pickup_request(request,pickup_request_id):
    # get_pickup_request = get_object_or_404(pickup_request, id=pickup_request_id)
    delete_pickup_requests = pickup_request.objects.get(id=pickup_request_id)
    delete_pickup_requests.delete()
    return redirect("pickups:display_pickup_requests")
