from PIL import Image
from django.db import models

# Create your models here.

# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

from django.urls import reverse

# 引入富文本框


# 栏目的model
from taggit.managers import TaggableManager


class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章的阅读量
    total_views = models.PositiveIntegerField(default=0)

    # 文章作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body_content = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)

    # 文章的栏目 一对多外键关系
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created_time' 表明数据应该以倒序排列
        ordering = ('-created_time',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的save功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定图片大小宽度
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_inmage = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_inmage.save(self.avatar.path)

        return article

    # 测试演示
    def was_created_recently(self):
        # 若文章是“最近”发表的，则返回True
        diff = timezone.now() - self.created_time
        # if diff.days <= 0 and diff.days < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False



