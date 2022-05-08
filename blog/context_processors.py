from blog.models import Category, Tag
from django.db.models import Count, Q


def common(request):
    context = {
        'categories':Category.objects.annotate(
            count=Count('post',Q(post__is_published=True))
        ),
        'tags':Tag.objects.all()
    }
    return context
