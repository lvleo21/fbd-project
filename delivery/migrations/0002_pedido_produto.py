# Generated by Django 2.2.7 on 2019-11-18 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('obsevacoes', models.TextField()),
                ('data_validade', models.DateTimeField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery.Pessoa')),
                ('produtos', models.ManyToManyField(to='delivery.Produto')),
            ],
            options={
                'verbose_name_plural': 'Pedidos',
            },
        ),
    ]
