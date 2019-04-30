import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadDetail
from blog.models import Blog

today = timezone.now().date()
# 获取热门博客
def get_today_hot_blogs(content_type):
    today_hot_blogs = ReadDetail.objects.filter(content_type = content_type, read_date = today).order_by('-read_num')
    return today_hot_blogs[:7]

def get_yesterday_hot_blogs(content_type):
    yesterday = today - datetime.timedelta(days = 1)
    yesterday_hot_blogs = ReadDetail.objects.filter(content_type = content_type, read_date = yesterday).order_by('-read_num')
    return yesterday_hot_blogs[:7]

def get_one_week_hot_blogs():
    one_week_ago = today - datetime.timedelta(days = 7)
    one_week_hot_blogs = Blog.objects.filter(read_detail__read_date__lte = today, read_detail__read_date__gt = one_week_ago) \
                                    .values('id', 'title') \
                                    .annotate(read_num_sum = Sum('read_detail__read_num')) \
                                    .order_by("-read_num_sum")
    return one_week_hot_blogs[:7]

# 近7天阅读数据
def get_seven_read_blogs_data():
    date_dict = []
    read_num_sum_dict = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days = i)
        date_dict.append(date.strftime("%m/%d"))
        read_num_sum = ReadDetail.objects.filter(read_date = date) \
                                    .aggregate(Sum('read_num'))
        read_num_sum_dict.append(read_num_sum["read_num__sum"] or 0)
    return date_dict, read_num_sum_dict