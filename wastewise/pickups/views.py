from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import pickup_request
from .forms import CreatePickUpRequestForm, Update_pickup_requestForm

# --- DRF IMPORTS ---
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PickUpRequestSerializer


# ==========================================
# 1. LIST & DISPLAY REQUESTS
# ==========================================

# Template View
def pickup_request_views(request):
    pickup_requests = pickup_request.objects.all().order_by('-id')
    p = Paginator(pickup_requests, 5)
    page_num = request.GET.get('page', 2)
    page = p.get_page(page_num)
    context = {
        'pickup_requests': pickup_requests,
        'page': page
    }
    return render(request, 'pickups/display_pickup_requests.html', context)

# API Endpoint
@api_view(['GET'])
def api_pickup_request_list(request):
    pickup_requests = pickup_request.objects.all().order_by('-id')
    serializer = PickUpRequestSerializer(pickup_requests, many=True)
    return Response(serializer.data)


# ==========================================
# 2. CREATE REQUESTS
# ==========================================

# Template View
def place_pickUp_request_Views(request):
    if request.method == "POST":
        make_pickup_request = CreatePickUpRequestForm(request.POST)
        if make_pickup_request.is_valid():
            make_pickup_request.save()
            return redirect("pickups:display_pickup_requests")
    else:
        make_pickup_request = CreatePickUpRequestForm()
    
    context = {"make_pickup_request": make_pickup_request}
    return render(request, "pickups/make_pickup_request.html", context)

# API Endpoint
@api_view(['POST'])
def api_place_pickup_request(request):
    serializer = PickUpRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# 3. UPDATE REQUESTS
# ==========================================

# Template View
def update_pickup_requests(request, pickup_request_id):
    get_pickup_request = get_object_or_404(pickup_request, id=pickup_request_id)
    if request.method == "POST":
        update_pickup_request = Update_pickup_requestForm(request.POST, instance=get_pickup_request)
        if update_pickup_request.is_valid():
            update_pickup_request.save()
            return redirect("pickups:display_pickup_requests")
    else:
        update_pickup_request = Update_pickup_requestForm(instance=get_pickup_request)
        
    context = {"update_pickup_request": update_pickup_request}
    return render(request, "pickups/update_pickup_request.html", context)

# API Endpoint
@api_view(['PUT', 'PATCH'])
def api_update_pickup_request(request, pickup_request_id):
    get_pickup_request = get_object_or_404(pickup_request, id=pickup_request_id)
    # partial=True allows PATCH requests to modify only a few fields
    serializer = PickUpRequestSerializer(get_pickup_request, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# 4. DELETE REQUESTS
# ==========================================

# Template View
def delete_pickup_request(request, pickup_request_id):
    delete_pickup_requests = get_object_or_404(pickup_request, id=pickup_request_id)
    delete_pickup_requests.delete()
    return redirect("pickups:display_pickup_requests")

# API Endpoint
@api_view(['DELETE'])
def api_delete_pickup_request(request, pickup_request_id):
    delete_pickup_requests = get_object_or_404(pickup_request, id=pickup_request_id)
    delete_pickup_requests.delete()
    return Response({"message": "Pickup request deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
