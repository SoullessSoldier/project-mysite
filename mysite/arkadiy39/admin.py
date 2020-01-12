from django.contrib import admin

# Register your models here.
from .models import Books,Rubric

class BooksAdmin(admin.ModelAdmin):
    list_display=('rubric','date','pubdate','year','author','title','pages','format','size','quality','language','crc32','description','link','category','downloaded','file')
    list_display_links=('author','rubric',)
    search_fields=('author','title',)
admin.site.register(Books,BooksAdmin)
admin.site.register(Rubric)
