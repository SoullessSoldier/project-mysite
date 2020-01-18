from django.shortcuts import render
from django.http import HttpResponse
from .models import Books,Rubric

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
    context={'books':books,'rubrics':rubrics,'curent_rubric':current_rubric}
    return render(request,'arkadiy39/books_by_rubric.html',context)
