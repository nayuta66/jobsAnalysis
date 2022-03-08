from django.contrib import admin
from .models import JobdataClean, JobNumData, Statistics


# Register your models here.

@admin.register(JobdataClean)
class JobdataAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'category', 'job_fun', 'job_name', 'company_name', 'work_place', 'work_time', 'edu', 'job_num_details',
    'salary')
    list_display_links = ('id',)
    fields = (
    'category', 'job_fun', 'job_name', 'company_name', 'work_place', 'work_time', 'edu', 'job_num_details',
    'release_time', 'salary', 'practice_mode')


@admin.register(JobNumData)
class JobNumDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'job_fun', 'detail_type', 'num')
    list_display_links = ('id', 'category')
    fields = ('category', 'job_fun', 'detail_type', 'num')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'job_fun', 'work_place', 'work_time', 'edu', 'salary')
    list_display_links = ('id',)
    fields = ('category', 'job_fun', 'work_place', 'work_time', 'edu', 'salary')
