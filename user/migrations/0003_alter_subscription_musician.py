# Generated by Django 4.2.3 on 2023-07-07 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_image_alter_musicianprofile_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='musician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.musicianprofile', verbose_name='Музыкант'),
        ),
    ]
