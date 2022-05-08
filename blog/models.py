from distutils.command.upload import upload
from tabnanny import verbose
from unicodedata import category
from unittest import mock
from django.db import models
from django.forms import model_to_dict
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.


class Tag(models.Model):
    name = models.CharField('タグ',max_length=255)
    slug = models.SlugField('URL',unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'

class Category(models.Model):
    name = models.CharField('カテゴリー',max_length=255)
    slug = models.SlugField('URL',unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'

class Post(models.Model):
    title = models.CharField('タイトル',max_length=200)
    content = MarkdownxField('本文')
    image = models.ImageField('画像', upload_to='uploads/',null=True, blank=True)
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    updated_at = models.DateTimeField('更新日',auto_now=True)
    is_published = models.BooleanField('公開設定',default=False)

    category = models.ForeignKey(
        Category,verbose_name='カテゴリ' ,on_delete=models.PROTECT, null=True, blank=True
        )
    tags = models.ManyToManyField(
        Tag,verbose_name='タグ',blank=True
    )

    def convert_markdown_to_html(self):
        return markdownify(self.content)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

class Comment(models.Model):
    name = models.CharField('名前', max_length=100)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    post = models.ForeignKey(Post, verbose_name='記事', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]
    
    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'
    
class Reply(models.Model):
    name = models.CharField('名前', max_length=100)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    comment = models.ForeignKey(Comment, verbose_name='コメント', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]
    
    class Meta:
        verbose_name = '返信'
        verbose_name_plural = '返信'
    