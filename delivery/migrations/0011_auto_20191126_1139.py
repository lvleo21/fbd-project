# Generated by Django 2.2.7 on 2019-11-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0010_auto_20191126_0836'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name_plural': "Delivery's"},
        ),
        migrations.AddField(
            model_name='delivery',
            name='descricao',
            field=models.TextField(default=1, verbose_name='Descrição'),
            preserve_default=False,
        ),
    ]