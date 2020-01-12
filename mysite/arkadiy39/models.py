from django.db import models

# Create your models here.
class Books(models.Model):
    rubric=models.ForeignKey('Rubric',null=True,on_delete=models.PROTECT,verbose_name='Рубрика')
    date=models.CharField(max_length=50)
    pubdate=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    pages=models.CharField(max_length=50,null=True,blank=True)
    format=models.CharField(max_length=50,null=True,blank=True)
    size=models.CharField(max_length=50,null=True,blank=True)
    quality=models.CharField(max_length=50,null=True,blank=True)
    language=models.CharField(max_length=50,null=True,blank=True)
    crc32=models.CharField(max_length=50,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    link=models.TextField(null=True,blank=True)
    category=models.TextField(null=True,blank=True)
    downloaded=models.IntegerField(default=0)
    file=models.CharField(null=True,max_length=100)
    
    class Meta:
       verbose_name_plural="Книги"
       verbose_name="Книга"
       ordering=['-pubdate']
    
    def __str__(self):
        return self.title 


class Rubric(models.Model):
    name=models.CharField(max_length=20,db_index=True,verbose_name='Название')
    
    class Meta:
       verbose_name_plural="Рубрики"
       verbose_name="Рубрика"
       ordering=['name']

    def __str__(self):
        return self.name    