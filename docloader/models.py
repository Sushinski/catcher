# -*- coding: utf-8 -*-
from django.db import models


class CompanyRecord(models.Model):
    name = models.TextField(verbose_name=u'Компания')


class FlatRecord(models.Model):
    price = models.DecimalField(verbose_name=u'Цена', max_digits=19, decimal_places=10)
    district = models.TextField(verbose_name=u'Район', null=False)
    rooms = models.IntegerField(verbose_name=u'Кол-во комнат', null=False)
    area = models.FloatField(verbose_name=u'Площадь', null=False)
    company = models.ForeignKey(CompanyRecord, verbose_name=u'Компания', null=True)
    related_info = models.TextField(verbose_name=u'Дополнительно', null=True)
