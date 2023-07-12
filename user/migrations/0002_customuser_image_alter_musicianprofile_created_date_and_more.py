# Generated by Django 4.2.3 on 2023-07-07 07:56

import Stream.yandex_s3_storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.FileField(blank=True, null=True, storage=Stream.yandex_s3_storage.ClientDocsStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='musicianprofile',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='musicianprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_date', models.DateTimeField(auto_now_add=True)),
                ('musician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='musician', to='user.musicianprofile', verbose_name='Музыкант')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]