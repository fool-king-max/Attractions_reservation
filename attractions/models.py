from django.db import models

# Create your models here.


from django.db import models
from users.models import User

class Province(models.Model):
    # 定义省份列表
    PROVINCE_CHOICES = [
        ('北京', 'Beijing'),
        ('天津', 'Tianjin'),
        ('河北', 'Hebei'),
        ('山西', 'Shanxi'),
        ('内蒙古', 'Neimenggu'),
        ('辽宁', 'Liaoning'),
        ('吉林', 'Jilin'),
        ('黑龙江', 'Heilongjiang'),
        ('上海', 'Shanghai'),
        ('江苏', 'Jiangsu'),
        ('浙江', 'Zhejiang'),
        ('安徽', 'Anhui'),
        ('福建', 'Fujian'),
        ('江西', 'Jiangxi'),
        ('山东', 'Shandong'),
        ('河南', 'Henan'),
        ('湖北', 'Hubei'),
        ('湖南', 'Hunan'),
        ('广东', 'Guangdong'),
        ('广西', 'Guangxi'),
        ('海南', 'Hainan'),
        ('重庆', 'Chongqing'),
        ('四川', 'Sichuan'),
        ('贵州', 'Guizhou'),
        ('云南', 'Yunnan'),
        ('西藏', 'Xizang'),
        ('陕西', 'Shaanxi'),
        ('甘肃', 'Gansu'),
        ('青海', 'Qinghai'),
        ('宁夏', 'Ningxia'),
        ('新疆', 'Xinjiang'),
        ('台湾', 'Taiwan'),
        ('香港', 'Hongkong'),
        ('澳门', 'Macau')
    ]

    name = models.CharField(max_length=50, choices=PROVINCE_CHOICES,unique=True)
    zh_name = models.CharField(max_length=50,default="北京")
    def __str__(self):
        return self.zh_name

class Attraction(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name="景点名称")
    description = models.TextField(verbose_name="景点描述")
    location = models.CharField(max_length=100, verbose_name="景点位置")  # 可以添加详细位置描述
    province_name = models.ForeignKey(Province,to_field='name', on_delete=models.CASCADE ,verbose_name="所属省份")  # 新增字段，用于记录省份信息
    image = models.ImageField(upload_to='attractions/', verbose_name="展示图片")  # 新增字段，用于上传图片
    total_price = models.BigIntegerField(default=0,verbose_name="门票价格")
    manager = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User,to_field="id", on_delete=models.CASCADE)  # 用户
    attraction = models.ForeignKey(Attraction,to_field="id", on_delete=models.CASCADE)  # 预订的景点
    date = models.DateField()  # 预订日期
    time = models.TimeField()  # 预订时间
    num_people = models.BigIntegerField(default=1,verbose_name='预定人数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 总价格
    contact_name = models.CharField(max_length=100)  # 联系人姓名
    contact_phone = models.CharField(max_length=20)  # 联系人电话
    note = models.CharField(max_length=1000,default="",verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True)  # 预订创建时间
    is_paid = models.BooleanField(default=False,verbose_name="支付状态")  # 支付状态
    payment_date = models.DateTimeField(null=True, blank=True)  # 支付时间
    status = models.CharField(max_length=10,choices=[("approved", "同意"), ("rejected", "拒绝")],default=None,null=True,verbose_name="预约状态")

    # 预约状态
    def __str__(self):
        return f"{self.user.username} - {self.attraction.name} on {self.date} 支付状态:{self.is_paid} on {self.payment_date}"


class Review(models.Model):
    attraction = models.ForeignKey(Attraction, to_field="id",on_delete=models.CASCADE)  # 评论的景点
    name = models.ForeignKey(User,to_field="username", on_delete=models.CASCADE)  # 评论用户
    rating = models.PositiveIntegerField()  # 评分（1 到 5）
    comment = models.TextField()  # 评论内容
    created_at = models.DateTimeField(auto_now_add=True)  # 评论创建时间

    def __str__(self):
        return f"{self.name} - {self.attraction} ({self.rating})"

