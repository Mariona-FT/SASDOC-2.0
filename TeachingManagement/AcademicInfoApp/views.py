from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Field
from .forms import FieldForm

# Create your views here.

### FIELD ###
def field_crud(request):
    fields = Field.objects.all()
    form = FieldForm()
    deleting = None

    # Handle editing
    if 'edit' in request.GET:
        field = get_object_or_404(Field, pk=request.GET['edit'])
        form = FieldForm(instance=field)

    # Handle deletion confirmation
    if 'delete' in request.GET:
        deleting = get_object_or_404(Field, pk=request.GET['delete'])

    # Handle form submission (create/update)
    if request.method == 'POST':
        if 'edit' in request.GET:
            field = get_object_or_404(Field, pk=request.GET['edit'])
            form = FieldForm(request.POST, instance=field)
        else:
            form = FieldForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('field_crud')

    # Handle actual deletion
    if request.method == 'POST' and 'confirm_delete' in request.POST:
        deleting.delete()
        return redirect('field_crud')

    return render(request, 'field_crud.html', {
        'fields': fields,
        'form': form,
        'deleting': deleting
    })