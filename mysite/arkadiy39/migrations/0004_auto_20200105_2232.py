# Generated by Django 2.2.7 on 2020-01-05 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkadiy39', '0003_auto_20200105_2155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='books',
            options={'ordering': ['-pubdate'], 'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AlterField(
            model_name='books',
            name='downloaded',
            field=models.IntegerField(default=0),
        ),
    ]
