import decimal
from django.shortcuts import render
from .models import Statistics
from django.db import connection
from django.http import HttpResponse
import json


# Create your views here.

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def my_custom_sql(t, category, job_fun):
    with connection.cursor() as cursor:
        if job_fun == '':
            if t == 'salary':
                cursor.execute("SELECT AVG(salary) FROM statistics WHERE category='%s'" % category)
            elif t == 'edu':
                cursor.execute("SELECT AVG(edu) FROM statistics WHERE category='%s'" % category)
            elif t == 'worktime':
                cursor.execute("SELECT AVG(work_time) FROM statistics WHERE category='%s'" % category)
            elif t == 'need':
                cursor.execute("SELECT AVG(num) FROM job_num_data WHERE category='%s'" % category)
            row = cursor.fetchone()
        else:
            if t == 'salary':
                cursor.execute(
                    "SELECT AVG(salary) FROM statistics WHERE category='%s' and job_fun='%s'" % (category, job_fun))
            elif t == 'edu':
                cursor.execute(
                    "SELECT AVG(edu) FROM statistics WHERE category='%s'and job_fun='%s'" % (category, job_fun))
            elif t == 'worktime':
                cursor.execute(
                    "SELECT AVG(work_time) FROM statistics WHERE category='%s'and job_fun='%s'" % (category, job_fun))
            elif t == 'need':
                cursor.execute(
                    "SELECT AVG(num) FROM job_num_data WHERE category='%s'and job_fun='%s'" % (category, job_fun))
            row = cursor.fetchone()
    return row[0]


def index(request):
    return render(request, 'index.html')


def association(request):
    return render(request, 'association.html')


def salary(request):
    ll = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': []}
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l = []
        qs = Statistics.objects.filter(category=item)
        for i in qs:
            if i.job_fun not in l:
                l.append(i.job_fun)
        for i in l:
            ll[item].append(my_custom_sql('salary', item, i))
    data = {"answer": {"type": 'salary', "d": ll}}
    return render(request, 'total.html', data)


def salary_1(request):
    l = []
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l.append(my_custom_sql('salary', item, ''))
    data = {"answer": {"type": 'salary_1', "d": l}}
    return render(request, '1.html', context=data)


def salary_2(request):
    category = ''
    if request.body == b'a' or request.body == b'aa':
        category = 'a'
    if request.body == b'b':
        category = 'b'
    if request.body == b'c':
        category = 'c'
    if request.body == b'd':
        category = 'd'
    if request.body == b'e':
        category = 'e'
    if request.body == b'f':
        category = 'f'
    if request.body == b'g':
        category = 'g'
    if request.body == b'h':
        category = 'h'
    if request.body == b'i':
        category = 'i'
    if request.body == b'j':
        category = 'j'
    if request.body == b'k':
        category = 'k'
    l = []
    ll = []
    qs = Statistics.objects.filter(category=category)
    for i in qs:
        if i.job_fun not in l:
            l.append(i.job_fun)
    for item in l:
        ll.append(my_custom_sql('salary', category, item))
    data = {"answer": {"type": 'salary_2', "d": ll}}
    if request.body == b'aa':
        return render(request, '2.html', context=data)
    else:
        return HttpResponse(json.dumps(data))


def edu(request):
    ll = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': []}
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l = []
        qs = Statistics.objects.filter(category=item)
        for i in qs:
            if i.job_fun not in l:
                l.append(i.job_fun)
        for i in l:
            ll[item].append(my_custom_sql('edu', item, i))
    data = {"answer": {"type": 'edu', "d": ll}}
    return render(request, 'total.html', context=data)


def edu_1(request):
    l = []
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l.append(my_custom_sql('edu', item, ''))
    data = {"answer": {"type": 'edu_1', "d": l}}
    return render(request, '1.html', context=data)


def edu_2(request):
    category = ''
    if request.body == b'a' or request.body == b'aa':
        category = 'a'
    if request.body == b'b':
        category = 'b'
    if request.body == b'c':
        category = 'c'
    if request.body == b'd':
        category = 'd'
    if request.body == b'e':
        category = 'e'
    if request.body == b'f':
        category = 'f'
    if request.body == b'g':
        category = 'g'
    if request.body == b'h':
        category = 'h'
    if request.body == b'i':
        category = 'i'
    if request.body == b'j':
        category = 'j'
    if request.body == b'k':
        category = 'k'
    l = []
    ll = []
    qs = Statistics.objects.filter(category=category)
    for i in qs:
        if i.job_fun not in l:
            l.append(i.job_fun)
    for item in l:
        ll.append(my_custom_sql('edu', category, item))
    data = {"answer": {"type": 'edu_2', "d": ll}}
    if request.body == b'aa':
        return render(request, '2.html', context=data)
    else:
        return HttpResponse(json.dumps(data, cls=DecimalEncoder))


def worktime(request):
    ll = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': []}
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l = []
        qs = Statistics.objects.filter(category=item)
        for i in qs:
            if i.job_fun not in l:
                l.append(i.job_fun)
        for i in l:
            ll[item].append(my_custom_sql('worktime', item, i))
    data = {"answer": {"type": 'worktime', "d": ll}}
    return render(request, 'total.html', context=data)


def worktime_1(request):
    l = []
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l.append(my_custom_sql('worktime', item, ''))
    data = {"answer": {"type": 'worktime_1', "d": l}}
    return render(request, '1.html', context=data)


def worktime_2(request):
    category = ''
    if request.body == b'a':
        category = 'a'
    if request.body == b'b':
        category = 'b'
    if request.body == b'c':
        category = 'c'
    if request.body == b'd':
        category = 'd'
    if request.body == b'e':
        category = 'e'
    if request.body == b'f':
        category = 'f'
    if request.body == b'g':
        category = 'g'
    if request.body == b'h':
        category = 'h'
    if request.body == b'i':
        category = 'i'
    if request.body == b'j':
        category = 'j'
    if request.body == b'k':
        category = 'k'
    l = []
    ll = []
    qs = Statistics.objects.filter(category=category)
    for i in qs:
        if i.job_fun not in l:
            l.append(i.job_fun)
    for item in l:
        ll.append(my_custom_sql('worktime', category, item))
    data = {"answer": {"type": 'worktime_2', "d": ll}}
    if request.body == b'aa':
        return render(request, '2.html', context=data)
    else:
        return HttpResponse(json.dumps(data, cls=DecimalEncoder))


def need(request):
    ll = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': []}
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l = []
        qs = Statistics.objects.filter(category=item)
        for i in qs:
            if i.job_fun not in l:
                l.append(i.job_fun)
        for i in l:
            ll[item].append(my_custom_sql('need', item, i))
    data = {"answer": {"type": 'need', "d": ll}}
    return render(request, 'total.html', context=data)


def need_1(request):
    l = []
    for item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']:
        l.append(my_custom_sql('need', item, ''))
    data = {"answer": {"type": 'need_1', "d": l}}
    return render(request, '1.html', context=data)


def need_2(request):
    category = ''
    if request.body == b'a':
        category = 'a'
    if request.body == b'b':
        category = 'b'
    if request.body == b'c':
        category = 'c'
    if request.body == b'd':
        category = 'd'
    if request.body == b'e':
        category = 'e'
    if request.body == b'f':
        category = 'f'
    if request.body == b'g':
        category = 'g'
    if request.body == b'h':
        category = 'h'
    if request.body == b'i':
        category = 'i'
    if request.body == b'j':
        category = 'j'
    if request.body == b'k':
        category = 'k'
    l = []
    ll = []
    qs = Statistics.objects.filter(category=category)
    for i in qs:
        if i.job_fun not in l:
            l.append(i.job_fun)
    for item in l:
        ll.append(my_custom_sql('need', category, item))
    data = {"answer": {"type": 'need_2', "d": ll}}
    if request.body == b'aa':
        return render(request, '2.html', context=data)
    else:
        return HttpResponse(json.dumps(data, cls=DecimalEncoder))


def city(request):
    l = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT AVG(salary) FROM statistics WHERE work_place='北京'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(edu) FROM statistics WHERE work_place='北京'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(work_time) FROM statistics WHERE work_place='北京'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT count(*) FROM statistics WHERE work_place='北京'")
        row = cursor.fetchone()
        l.append(row[0])

        cursor.execute("SELECT AVG(salary) FROM statistics WHERE work_place='上海'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(edu) FROM statistics WHERE work_place='上海'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(work_time) FROM statistics WHERE work_place='上海'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT count(*) FROM statistics WHERE work_place='上海'")
        row = cursor.fetchone()
        l.append(row[0])

        cursor.execute("SELECT AVG(salary) FROM statistics WHERE work_place='广州'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(edu) FROM statistics WHERE work_place='广州'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(work_time) FROM statistics WHERE work_place='广州'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT count(*) FROM statistics WHERE work_place='广州'")
        row = cursor.fetchone()
        l.append(row[0])

        cursor.execute("SELECT AVG(salary) FROM statistics WHERE work_place='深圳'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(edu) FROM statistics WHERE work_place='深圳'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT AVG(work_time) FROM statistics WHERE work_place='深圳'")
        row = cursor.fetchone()
        l.append(row[0])
        cursor.execute("SELECT count(*) FROM statistics WHERE work_place='深圳'")
        row = cursor.fetchone()
        l.append(row[0])
    data = {"answer": l}
    return render(request, 'city.html', context=data)


def introduction(request):
    return render(request, 'introduction.html')
