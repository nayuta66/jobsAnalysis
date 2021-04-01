"""job51 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from analysis.views import index, association, salary, salary_1, salary_2, edu, edu_1, edu_2, worktime, worktime_1, \
    worktime_2, need, need_1, need_2, city, introduction

urlpatterns = [
    url(r'^$', index),
    url(r'^association/$', association),
    url(r'^salary/$', salary),
    url(r'^salary_1/$', salary_1),
    url(r'^salary_2/$', salary_2),
    url(r'^edu/$', edu),
    url(r'^edu_1/$', edu_1),
    url(r'^edu_2/$', edu_2),
    url(r'^worktime/$', worktime),
    url(r'^worktime_1/$', worktime_1),
    url(r'^worktime_2/$', worktime_2),
    url(r'^need/$', need),
    url(r'^need_1/$', need_1),
    url(r'^need_2/$', need_2),
    url(r'^city/$', city),
    url(r'^introduction/$', introduction),
    url(r'^admin/', admin.site.urls),
]
