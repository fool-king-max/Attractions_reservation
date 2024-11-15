# Generated by Django 2.2.10 on 2024-11-11 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='景点名称')),
                ('description', models.TextField(verbose_name='景点描述')),
                ('location', models.CharField(max_length=100, verbose_name='景点位置')),
                ('image', models.ImageField(upload_to='attractions/', verbose_name='展示图片')),
                ('total_price', models.BigIntegerField(default=0, verbose_name='门票价格')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('beijing', '北京'), ('tianjin', '天津'), ('hebei', '河北'), ('shanxi', '山西'), ('neimenggu', '内蒙古'), ('liaoning', '辽宁'), ('jilin', '吉林'), ('heilongjiang', '黑龙江'), ('shanghai', '上海'), ('jiangsu', '江苏'), ('zhejiang', '浙江'), ('anhui', '安徽'), ('fujian', '福建'), ('jiangxi', '江西'), ('shandong', '山东'), ('henan', '河南'), ('hubei', '湖北'), ('hunan', '湖南'), ('guangdong', '广东'), ('guangxi', '广西'), ('hainan', '海南'), ('chongqing', '重庆'), ('sichuan', '四川'), ('guizhou', '贵州'), ('yunnan', '云南'), ('xizang', '西藏'), ('shanxi', '陕西'), ('gansu', '甘肃'), ('qinghai', '青海'), ('ningxia', '宁夏'), ('xinjiang', '新疆'), ('taiwan', '台湾'), ('hongkong', '香港'), ('macau', '澳门')], max_length=50, unique=True)),
                ('zh_name', models.CharField(default='北京', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('num_people', models.BigIntegerField(default=1, verbose_name='预定人数')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contact_name', models.CharField(max_length=100)),
                ('contact_phone', models.CharField(max_length=20)),
                ('note', models.CharField(default='', max_length=1000, verbose_name='备注')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='支付状态')),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('approved', '同意'), ('rejected', '拒绝')], default=None, max_length=10, null=True, verbose_name='预约状态')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attractions.Attraction')),
            ],
        ),
    ]
