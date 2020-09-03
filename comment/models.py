from django.db import models
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey, MPTTModel

from article.models import ArticlePost
# 引入富文本框
from ckeditor.fields import RichTextField


# Create your models here.
# 博文的评论 # 替换 models.Model 为 MPTTModel
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    # body_context = models.RichTextField()
    body_content = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    # 新增， mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增， 记录二级评论回复给谁
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created_time', )
    class MTTPMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body_content[:20]