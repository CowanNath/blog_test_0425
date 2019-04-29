from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'read_num')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'read_num', 'read_date')
