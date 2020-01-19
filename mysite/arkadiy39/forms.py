from django.forms import ModelForm

from .models import Books

class BookForm(ModelForm):
    class Meta:
        model = Books
        fields=('rubric', 'date', 'pubdate', 'year', 'author', 'title', 'pages', 'format','size', 'quality',
                'language', 'crc32','description', 'link', 'category', 'downloaded', 'file')