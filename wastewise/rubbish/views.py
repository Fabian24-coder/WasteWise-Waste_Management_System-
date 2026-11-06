from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import RubbishDetail
from .forms import RubbishDetailForm


def _is_admin(user):
    return user.role == 'admin' or user.is_superuser


@login_required
def rubbish_list(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden()
    items = RubbishDetail.objects.all()
    category = request.GET.get('category')
    q = request.GET.get('q')
    if category:
        items = items.filter(category=category)
    if q:
        items = items.filter(name__icontains=q)
    return render(request, 'rubbish/list.html', {
        'items': items,
        'categories': RubbishDetail.CATEGORY_CHOICES,
        'active_page': 'waste',
    })



@login_required
def rubbish_create(request):
    if not _is_admin(request.user):
        return HttpResponseForbidden()
    form = RubbishDetailForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Waste type added.')
        return redirect('rubbish_list')
    return render(request, 'rubbish/form.html', {
        'form': form,
        'title': 'Add waste type',
        'active_page': 'waste',
    })


@login_required
def rubbish_update(request, pk):
    if not _is_admin(request.user):
        return HttpResponseForbidden()
    item = get_object_or_404(RubbishDetail, pk=pk)
    form = RubbishDetailForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Waste type updated.')
        return redirect('rubbish_list')
    return render(request, 'rubbish/form.html', {
        'form': form,
        'title': 'Edit waste type',
        'active_page': 'waste',
    })


@login_required
@require_POST
def rubbish_toggle(request, pk):
    """Deactivate/reactivate instead of deleting, to keep history safe."""
    if not _is_admin(request.user):
        return HttpResponseForbidden()
    item = get_object_or_404(RubbishDetail, pk=pk)
    item.is_active = not item.is_active
    item.save()
    return redirect('rubbish_list')
