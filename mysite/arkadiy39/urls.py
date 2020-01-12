from django.urls import path
from .views import index,books,books_by_rubric
urlpatterns=[
     path('books/<int:rubric_id>',books_by_rubric),
     path('books/',books),
     path('',index),
]