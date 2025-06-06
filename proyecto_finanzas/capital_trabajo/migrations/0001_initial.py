# Generated by Django 5.2.1 on 2025-06-02 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicadorCapitalTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoIndicador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('indicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capital_trabajo.indicadorcapitaltrabajo')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.periodo')),
            ],
            options={
                'unique_together': {('indicador', 'periodo')},
            },
        ),
    ]
