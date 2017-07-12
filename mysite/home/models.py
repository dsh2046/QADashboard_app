from __future__ import unicode_literals
from django.db import connection
from django.db import models


class product(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class functional_testcase(models.Model):
    test_name = models.CharField(max_length=128)
    test_type = models.CharField(max_length=32)
    test_comment = models.CharField(max_length=128)

    def __unicode__(self):
        return self.test_name


class functional_test_run(models.Model):
    name = models.CharField(max_length=32)
    product = models.ForeignKey(product)
    os = models.CharField(max_length=8)
    test_type = models.CharField(max_length=32)
    build_info = models.CharField(max_length=16)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_ran = models.IntegerField()
    total_passed = models.IntegerField()
    total_failed = models.IntegerField()
    status = models.IntegerField()

    def __unicode__(self):
        return self.name


class functional_results(models.Model):
    job = models.ForeignKey(functional_test_run)
    test = models.ForeignKey(functional_testcase)
    test_result = models.CharField(max_length=128)
    area = models.CharField(max_length=128, default='')
    log_file = models.CharField(max_length=256)
    start_time = models.CharField(max_length=128)
    end_time = models.CharField(max_length=128)

    def __unicode__(self):
        return self.test_result


class performance_testcase(models.Model):
    test_name = models.CharField(max_length=128)
    test_component = models.IntegerField()
    test_comment = models.CharField(max_length=128)

    def __unicode__(self):
        return self.test_name


class performance_test_run(models.Model):
    name = models.CharField(max_length=32)
    product = models.ForeignKey(product)
    os = models.CharField(max_length=8)
    test_type = models.IntegerField()
    build_info = models.CharField(max_length=16)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_ran = models.IntegerField()
    total_passed = models.IntegerField()
    total_failed = models.IntegerField()
    status = models.IntegerField()

    def __unicode__(self):
        return self.name


class performance_results(models.Model):
    job = models.ForeignKey(performance_test_run)
    test = models.ForeignKey(performance_testcase)
    test_result = models.CharField(max_length=128)
    log_file = models.CharField(max_length=128)
    start_time = models.CharField(max_length=128)
    end_time = models.CharField(max_length=128)

    def __unicode__(self):
        return self.test_result









