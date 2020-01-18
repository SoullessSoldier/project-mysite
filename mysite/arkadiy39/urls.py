from django.urls import path
from .views import index,books_index,books_by_rubric
urlpatterns=[
     path('books/<int:rubric_id>',books_by_rubric,name='books_by_rubric'),
     path('books/',books_index,name='books_index'),
     path('',index),
]