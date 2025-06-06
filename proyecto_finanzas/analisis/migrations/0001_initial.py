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
            name='RazonFinanciera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('LIQUIDEZ', 'Liquidez'), ('ACTIVIDAD', 'Actividad'), ('ENDEUDAMIENTO', 'Endeudamiento'), ('RENTABILIDAD', 'Rentabilidad')], max_length=20)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnalisisHorizontal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variacion_absoluta', models.DecimalField(decimal_places=2, max_digits=15)),
                ('variacion_porcentual', models.DecimalField(decimal_places=2, max_digits=7)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.cuentacontable')),
                ('periodo_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_h', to='finanzas.periodo')),
                ('periodo_comparado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparado_h', to='finanzas.periodo')),
            ],
            options={
                'unique_together': {('cuenta', 'periodo_base', 'periodo_comparado')},
            },
        ),
        migrations.CreateModel(
            name='AnalisisVertical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=7)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.cuentacontable')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.periodo')),
            ],
            options={
                'unique_together': {('cuenta', 'periodo')},
            },
        ),
        migrations.CreateModel(
            name='ResultadoRazon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=4, max_digits=10)),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.periodo')),
                ('razon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analisis.razonfinanciera')),
            ],
            options={
                'unique_together': {('razon', 'periodo')},
            },
        ),
    ]
