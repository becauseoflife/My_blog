from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
# 引入富文本框
from ckeditor.fields import RichTextField


# Create your models here.
# 博文的评论
class Comment(models.Model):
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
    body_context = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_time', )

    def __str__(self):
        return self.body_context[:20]