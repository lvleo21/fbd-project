# Generated by Django 2.2.7 on 2019-12-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0023_auto_20191201_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria_produto',
            field=models.CharField(choices=[('refeicao', 'Refeição'), ('bebida', 'Bebida'), ('sobremesas', 'Sobremesa')], max_length=50, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
