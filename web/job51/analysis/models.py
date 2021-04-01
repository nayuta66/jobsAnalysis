# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class JobNumData(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True)
    job_fun = models.IntegerField(blank=True, null=True)
    detail_type = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'job_num_data'


class Jobdata(models.Model):
    category = models.CharField(max_length=8, blank=True, null=True)
    job_fun = models.IntegerField(blank=True, null=True)
    job_name = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128, blank=True, null=True)
    work_place = models.CharField(max_length=128, blank=True, null=True)
    work_time = models.CharField(max_length=128, blank=True, null=True)
    edu = models.CharField(max_length=128, blank=True, null=True)
    job_num_details = models.CharField(max_length=128, blank=True, null=True)
    release_time = models.CharField(max_length=128, blank=True, null=True)
    salary = models.CharField(max_length=128, blank=True, null=True)
    company_treatment_details = models.CharField(max_length=128, blank=True, null=True)
    practice_mode = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jobdata'


class JobdataClean(models.Model):
    category = models.CharField(max_length=8, blank=True, null=True)
    job_fun = models.IntegerField(blank=True, null=True)
    job_name = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128, blank=True, null=True)
    work_place = models.CharField(max_length=128, blank=True, null=True)
    work_time = models.CharField(max_length=128, blank=True, null=True)
    edu = models.CharField(max_length=128, blank=True, null=True)
    job_num_details = models.CharField(max_length=128, blank=True, null=True)
    release_time = models.CharField(max_length=128, blank=True, null=True)
    salary = models.CharField(max_length=128, blank=True, null=True)
    company_treatment_details = models.CharField(max_length=128, blank=True, null=True)
    practice_mode = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jobdata_clean'


class Statistics(models.Model):
    category = models.CharField(max_length=8, blank=True, null=True)
    job_fun = models.IntegerField(blank=True, null=True)
    work_place = models.CharField(max_length=128, blank=True, null=True)
    work_time = models.FloatField(blank=True, null=True)
    edu = models.IntegerField(blank=True, null=True)
    salary = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'statistics'
