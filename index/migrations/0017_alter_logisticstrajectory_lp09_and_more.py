# Generated by Django 4.1.8 on 2024-07-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_alter_logisticstrajectory_lp03_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logisticstrajectory',
            name='LP09',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='终点经纬度'),
        ),
        migrations.AlterField(
            model_name='logisticstrajectory',
            name='LP10',
            field=models.CharField(blank=True, default='', max_length=400, verbose_name='终点地址'),
        ),
    ]
