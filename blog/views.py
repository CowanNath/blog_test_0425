from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType


def blog_list(request):
    blogs = Blog.objects.all()
    blog_types = BlogType.objects.all()
    blog_dates = Blog.objects.dates("created_time", "month", order="ASC" )

    paginator = Paginator(blogs, 10)
    page_num = request.GET.get('page', 1)
    blogs_of_page = paginator.get_page(page_num)

    context = {}
    context["blogs_of_page"] = blogs_of_page
    context["page_range"] = blogs_of_page.paginator.page_range
    context["blog_types"] = blog_types
    context["blog_dates"] = blog_dates
    return render(request, 'blog_list.html', context)

def blogs_with_type(request, type_id):
    blog_type = get_object_or_404(BlogType, pk = type_id)
    blog_dates = Blog.objects.dates("created_time", "month", order="ASC" )
    blog_types = BlogType.objects.all()
    blogs = blog_type.blog.all()
    context = {}
    context["blogs"] = blogs
    context["blog_type"] = blog_type
    context["blog_types"] = blog_types
    context["blog_dates"] = blog_dates
    return render(request, 'blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs = Blog.objects.filter(created_time__year = year, created_time__month = month)
    context = {}
    context["blogs"] = blogs
    context["blog_date"] = "%d年%d月" % (year, month)
    return render(request, 'blogs_with_date.html', context) 

def blog_detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    context = {}
    context["blog"] = blog
    return render(request, 'blog_detail.html', context)