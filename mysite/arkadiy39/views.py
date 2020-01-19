from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Books,Rubric
from .forms import BookForm
import rss1
# Create your views here.
def index(request):
    return HttpResponse("Here will be books")


def books_index(request):
    books=Books.objects.order_by('-pubdate')
    rubrics=Rubric.objects.all()
    context={'books':books,'rubrics':rubrics}
    return render(request,'arkadiy39/books.html',context)
    
    
def books_by_rubric(request,rubric_id):
    books=Books.objects.filter(rubric=rubric_id)
    rubrics=Rubric.objects.all()
    current_rubric=Rubric.objects.get(pk=rubric_id)
    context={'books':books,'rubrics':rubrics,'current_rubric':current_rubric}
    return render(request,'arkadiy39/books_by_rubric.html',context)

class BooksCreateView(CreateView):
    template_name='arkadiy39/create.html'
    form_class = BookForm
    success_url = reverse_lazy('books_index')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context

def books_load(request):
    rubrics = Rubric.objects.all()
    context={'rubrics':rubrics,'result':rss1.main()}
    return render(request, 'arkadiy39/books_load.html', context)
