from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blog_list, name="blog_list"),
    path('<int:id>', views.blog_detail, name="blog_detail"),
    path('blog_type/<int:type_id>', views.blogs_with_type, name="blogs_with_type"),
    path('blog_date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date"),
]
