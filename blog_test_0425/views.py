from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_today_hot_blogs, get_yesterday_hot_blogs, get_one_week_hot_blogs, get_seven_read_blogs_data
from blog.models import Blog

def home(request):
    ct = ContentType.objects.get_for_model(Blog)
    date_dict, read_num_sum_dict = get_seven_read_blogs_data()

    # 获取一周热门博客缓存
    get_one_week_hot_blog = cache.get('get_one_week_hot_blog')
    if get_one_week_hot_blog is None:
        get_one_week_hot_blog = get_one_week_hot_blogs()
        cache.set('get_one_week_hot_blog', get_one_week_hot_blog, 3600)

    context = {}
    context["get_today_hot_blogs"] = get_today_hot_blogs(ct)
    context["get_yesterday_hot_blogs"] = get_yesterday_hot_blogs(ct)
    context["get_one_week_hot_blog"] = get_one_week_hot_blog
    context["date_dict"] = date_dict
    context["read_num_sum_dict"] = read_num_sum_dict
    return render(request, "home.html", context)