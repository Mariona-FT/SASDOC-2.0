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

    #Edit
    if 'edit' in request.GET:
        field = get_object_or_404(Field, pk=request.GET['edit'])
        form = FieldForm(instance=field)

    # Delete
    if 'delete' in request.GET:
        deleting = get_object_or_404(Field, pk=request.GET['delete'])

    # Handle form submission (create/update)
    if request.method == 'POST':
        if 'edit' in request.GET:
            field = get_object_or_404(Field, pk=request.GET['edit'])
            form = FieldForm(request.POST, instance=field)
        else:
            form = FieldForm(request.POST)
        
        #Create Field
        if form.is_valid():
            form.save()
            return redirect('field_crud')

    # Delete compleatly
    if request.method == 'POST' and 'confirm_delete' in request.POST:
        deleting.delete()
        return redirect('field_crud')

    #List of fields
    return render(request, 'field_crud.html', {
        'fields': fields,
        'form': form,
        'deleting': deleting
    })

def section_crud(request):
    pass

def section_crud(request):
    pass

def school_crud(request):
    pass

def degree_crud(request):
    pass

def course_crud(request):
    pass