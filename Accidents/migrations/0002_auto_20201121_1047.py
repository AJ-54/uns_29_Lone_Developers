# Generated by Django 3.0.11 on 2020-11-21 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accidents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accident',
            old_name='lattitude',
            new_name='latitude',
        ),
        migrations.RenameField(
            model_name='hospital',
            old_name='hospital_lattitude',
            new_name='hospital_latitude',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicle',
        ),
        migrations.AlterField(
            model_name='accident',
            name='hospital',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='accidents', to='Accidents.Hospital'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='vehicles',
            field=models.ManyToManyField(blank=True, null=True, to='Accidents.Vehicle'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='PredictAccident/images/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='number',
            field=models.CharField(max_length=256),
        ),
    ]
