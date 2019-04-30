from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Blog, BlogType
from read_statistics.models import ReadNum, ReadDetail

def get_common_data(blogs, request):
    # 分页器
    paginator = Paginator(blogs, 10)
    page_num = request.GET.get('page', 1)
    blogs_of_page = paginator.get_page(page_num)

    # 博客按照日期计数
    blog_dates = Blog.objects.dates("created_time", "month", order="ASC" )
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_date_count = Blog.objects.filter(created_time__year = blog_date.year, created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] = blog_date_count

    context = {}
    context["blogs_of_page"] = blogs_of_page
    context["page_range"] = blogs_of_page.paginator.page_range
    context["blog_types"] = BlogType.objects.annotate(blog_type_count = Count("blog")) # 博客按照分类计数
    context["blog_dates_dict"] = blog_dates_dict
    return context

def blog_list(request):
    blogs = Blog.objects.all()

    context = get_common_data(blogs, request)
    return render(request, 'blog_list.html', context)

def blogs_with_type(request, type_id):
    blog_type = get_object_or_404(BlogType, pk = type_id)
    blogs = blog_type.blog.all()

    context = get_common_data(blogs, request)
    context["blog_type"] = blog_type
    return render(request, 'blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs = Blog.objects.filter(created_time__year = year, created_time__month = month)

    context = get_common_data(blogs, request)
    context["blog_date"] = "%d年%d月" % (year, month)
    return render(request, 'blogs_with_date.html', context) 

def blog_detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    previous_blog = Blog.objects.filter(created_time__gt = blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt = blog.created_time).first()

    # 阅读计数
    ct = ContentType.objects.get_for_model(blog)
    if not request.COOKIES.get("%s_%s_read" % ("blog", blog.id)):

        # 总的阅读计数
        readNum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = blog.id)
        readNum.read_num += 1
        readNum.save()

        # 每日阅读计数
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type = ct, object_id = blog.id, read_date = date)
        readDetail.read_num += 1
        readDetail.save()

    context = {}
    context["blog"] = blog
    context["previous_blog"] = previous_blog
    context["next_blog"] = next_blog
    response = render(request, 'blog_detail.html', context)
    response.set_cookie("%s_%s_read" % ("blog", blog.id), 'true')
    return response