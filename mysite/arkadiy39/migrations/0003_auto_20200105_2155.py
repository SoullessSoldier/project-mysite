# Generated by Django 2.2.7 on 2020-01-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkadiy39', '0002_books_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='downloaded',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]