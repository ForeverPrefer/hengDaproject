from django.db import models

# Create your models here.
from django.utils import timezone

PRODUCTS_CHOICES = (
    ('家用机器人', '家用机器人'),
    ('智能监控', '智能监控'),
    ('人脸识别解决方案', '人脸识别解决方案'),
)

class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='产品标题')
    description = models.TextField(verbose_name='产品详情描述')
    productType = models.CharField(max_length=50, choices=PRODUCTS_CHOICES, verbose_name='产品类型')
    price = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True, verbose_name='产品价格')
    publishDate = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ('-publishDate',)
class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productImgs', verbose_name='产品')
    photo = models.ImageField(upload_to='Product/', blank=True, verbose_name='产品图片')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'