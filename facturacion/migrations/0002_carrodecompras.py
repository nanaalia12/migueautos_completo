# Generated by Django 4.1 on 2022-09-05 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0002_alter_insumo_marca'),
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrodecompras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insumo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='insumo.insumo', verbose_name='insumo')),
            ],
        ),
    ]
