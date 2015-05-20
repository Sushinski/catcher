# -*- coding: utf-8 -*-
from django.db import models


class CompanyRecord(models.Model):
    name = models.TextField(verbose_name=u'Компания')


class BuildingRecord(models.Model):
    company = models.ForeignKey(CompanyRecord, verbose_name=u'Компания', null=True)


class BuildingFieldRecord(models.Model):
    field = models.TextField(verbose_name=u'Название поля', null=False, unique=True)
    value = models.TextField(verbose_name=u'Значение поля', null=True)
    flat = models.ForeignKey(BuildingRecord, verbose_name=u'Дом', null=False)


class FlatRecord(models.Model):
    company = models.ForeignKey(BuildingRecord, verbose_name=u'Компания', null=True)


class FlatFieldRecord(models.Model):
    field = models.TextField(verbose_name=u'Название поля', null=False, unique=True)
    value = models.TextField(verbose_name=u'Значение поля', null=True)
    flat = models.ForeignKey(FlatRecord, verbose_name=u'Квартира', null=False)
