from django.urls import path
from .views import index,books_index,books_by_rubric
from .views import BooksCreateView
urlpatterns=[
     path('books/<int:rubric_id>',books_by_rubric,name='books_by_rubric'),
     path('books/',books_index,name='books_index'),
     path('books/add/',BooksCreateView.as_view(),name='add'),

     path('',index),
]