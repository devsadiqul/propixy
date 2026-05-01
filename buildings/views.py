from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Building, Unit
from .forms import BuildingForm, UnitForm


@login_required
def building_list(request):
    buildings = Building.objects.filter(user=request.user)
    return render(request, 'buildings/building_list.html', {'buildings': buildings})


@login_required
def building_create(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.user = request.user
            building.save()
            messages.success(request, f'Building "{building.name}" created successfully!')
            return redirect('building_list')
    else:
        form = BuildingForm()

    return render(request, 'buildings/building_form.html', {
        'form': form,
        'title': 'Add Building',
        'button_text': 'Create Building'
    })


@login_required
def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            messages.success(request, f'Building "{building.name}" updated successfully!')
            return redirect('building_list')
    else:
        form = BuildingForm(instance=building)

    return render(request, 'buildings/building_form.html', {
        'form': form,
        'building': building,
        'title': 'Edit Building',
        'button_text': 'Update Building'
    })


@login_required
def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk, user=request.user)

    if request.method == 'POST':
        name = building.name
        building.delete()
        messages.success(request, f'Building "{name}" deleted successfully!')
        return redirect('building_list')

    return render(request, 'buildings/building_confirm_delete.html', {'building': building})


@login_required
def unit_list(request):
    units = Unit.objects.filter(user=request.user).select_related('building')
    buildings = Building.objects.filter(user=request.user)

    building_id = request.GET.get('building')
    if building_id:
        units = units.filter(building_id=building_id)

    return render(request, 'buildings/unit_list.html', {
        'units': units,
        'buildings': buildings,
        'selected_building': building_id
    })


@login_required
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, user=request.user)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.user = request.user
            unit.save()
            messages.success(request, f'Unit "{unit.flat_number}" created successfully!')
            return redirect('unit_list')
    else:
        form = UnitForm(user=request.user)

    return render(request, 'buildings/unit_form.html', {
        'form': form,
        'title': 'Add Unit',
        'button_text': 'Create Unit'
    })


@login_required
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Unit "{unit.flat_number}" updated successfully!')
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit, user=request.user)

    return render(request, 'buildings/unit_form.html', {
        'form': form,
        'unit': unit,
        'title': 'Edit Unit',
        'button_text': 'Update Unit'
    })


@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk, user=request.user)

    if request.method == 'POST':
        flat_number = unit.flat_number
        unit.delete()
        messages.success(request, f'Unit "{flat_number}" deleted successfully!')
        return redirect('unit_list')

    return render(request, 'buildings/unit_confirm_delete.html', {'unit': unit})