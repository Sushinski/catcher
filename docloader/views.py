# -*- coding: utf-8 -*-
from django.shortcuts import render
from docloader.fileloader import Workbook
from catcher.settings import UPLOAD_DIR
from models import *


# todo ввод компания, этажность дома, адрес, район, срок сдачи, форма договора,  название комплекса, виды рассрочки,
# todo ипотека
wb = None
DOC_FIELDS = ('price', 'area', 'abs_area', 'district', 'rooms', 'floor', 'primary_fee', 'room_height',
              'kitchen_area', 'balcony')
DOC_RU_FIELDS = (u'Цена', u'Площадь', u'Общ. площадь', u'Район', u'Комнат', u'Этаж', u'Первый взнос', u'Потолок',
                 u'Пл. кухни', u'Балкон')
DOC_FIELDS_DICT = dict(zip(DOC_RU_FIELDS, DOC_FIELDS))

DOC_INPUT_FIELDS = [(u'building', u'Название объекта'), (u'house_floors', u'Этажность дома'), (u'address', u'Адрес'),
                    (u'district', u'Район'), (u'release_date', u'Срок сдачи'), (u'agreement_form', u'Форма договора'),
                    (u'payment_form', u'Виды рассрочки'), (u'mortgage', u'Ипотека')]


def upload_view(request):
    c = {'view': None, }
    return render(request, 'doc_upload_view.html', c)


def upload_result_view(request):
    view = None
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES['upl_file'])
        view = UploadResultView(filename)
    c = {'view': view, }
    return render(request, 'upload_result_view.html', c)


def handle_uploaded_file(f):
    name = UPLOAD_DIR + str(f)
    try:
        with open(name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return name
    except Exception as ex:
        print str(ex)
        return None


def flat_request_view(request):
    c = {'view': FlatRequestView()}
    return render(request, 'flat_request_form.html', c)


def flat_request_result_view(request):
    c = {'view': FlatRequestResultView()}
    return render(request, 'flat_request_result_form.html', None)


class FlatRequestView():
    def __init__(self):
        self.fields = zip(DOC_RU_FIELDS, DOC_FIELDS)


class FlatRequestResultView():
    def __init__(self, request):
        request_vals = dict()
        for name, id in zip(DOC_RU_FIELDS, DOC_FIELDS):  # collects field values
            request_vals[id] = request.POST.get(id, None)
        #  enquire db for collected
        res = list()
        res_qset = FlatRecord.objects.all().values_list('flat_id', flat=True)
        for key, value in request_vals:
            if value:
                res.extend(list(res_qset.filter(field=key, value=value)))
        #  get result view rows
        rows = FlatRecord.objects.filter(id__in=res).prefetch_related('flatfieldrecord')




class UploadResultView():
    def __init__(self, filename):
        self.sheets = []  # страницы, содержащие headlines - заголовки
        self.sel_options = zip(DOC_FIELDS, DOC_RU_FIELDS)  # варианты целевых полей в базе
        self.single_fields = [(u'company', u'Компания')]
        self.single_fields.extend(DOC_INPUT_FIELDS)
        global wb
        wb = Workbook(filename)
        self.wb = wb
        self.fields_num = 25
        # self.rows = zip(enumerate(wb.sheet_names()), wb.dimensions())
        # todo сделать анализ строк листов на заголовки
        sheet_names = wb.sheet_names()
        for sh in sheet_names:
            self.sheets.append((sh, self.get_sheet_lines(sh)))

    def get_sheet_lines(self, sheet_name):
        sheet = self.wb.get_sheet_by_name(sheet_name)
        res = [(i, enumerate(sheet.row_values(i, 0, self.fields_num))) for i in range(sheet.nrows)]
        return res


def parse_uploaded_file(request):
    global wb
    view = None
    if request.method == 'POST':
        view = ParseResultView(request)
    c = {'view': view, }
    return render(request, 'upload_result_view.html', c)


class ParseResultView():
    def __init__(self, request):
        global wb
        self.wb = wb
        self.fields_fmt = None
        self.fields_num = 25
        self.company = None  # company in proccess
        self.building = None  # building in proccess
        for sh in wb.sheets:  # for every table
            # 1st - create or get building
            self.save_company_building(sh.name, request)
            # 2st - save flat rows
            started = False
            for i in range(sh.nrows):
                row = sh.row_values(i, 0, self.fields_num)
                row_1st_sel = request.POST[u'{0}_{1}'.format(sh.name, i)]
                if row_1st_sel == 'header':
                    self.get_field_fmt(request, sh.name, i, row)
                elif row_1st_sel == 'start_range' and self.fields_fmt:
                    self.save_row_to_db(row, self.fields_fmt)
                    started = True
                elif row_1st_sel == 'end_range' and self.fields_fmt:
                    self.save_row_to_db(row, self.fields_fmt)
                    started = False
                elif self.fields_fmt and started:
                    self.save_row_to_db(row, self.fields_fmt)

    def save_company_building(self, sheet_name, request):
        try:
            self.company, cr = CompanyRecord.objects.get_or_create(name=request.POST[sheet_name+'_company'].lower())
            self.building, cr = BuildingRecord.objects.get_or_create(company=self.company,
                                                                     name=request.POST[sheet_name+'_building'].lower())
            if not cr:
                self.delete_building_objects()
            for fld, fld_name in DOC_INPUT_FIELDS:
                BuildingFieldRecord.objects.get_or_create(building=self.building, field=fld,
                                                          value=request.POST[sheet_name+'_'+fld])
        except Exception as ex:
            print ex

    def get_field_fmt(self, request, sheet_name, row_num, row):
        res = dict()
        for i, fld in enumerate(row):
            value = request.POST[u'sel_{0}_{1}_{2}'.format(sheet_name, row_num, i)]  # save fields mapping
            if value == "other":  # for not selected rows save field name
                res[i] = fld
            else:   # save mappings for selected
                res[value] = i
        self.fields_fmt = res

    def save_row_to_db(self, row, fields):
        try:
            flat = FlatRecord.objects.create(building=self.building)  # todo ключевые значения для квартиры
            for fld in DOC_FIELDS:  # save mapped fields
                value_key = fields.get(fld, None)
                value = row[value_key] if value_key else None
                FlatFieldRecord.objects.create(flat=flat,
                                               field=fld,
                                               value=value)
            for i, fld in enumerate(row):  # save unmapped fields
                value_key = fields.get(i, None)
                if value_key:
                    value = row[i]
                    FlatFieldRecord.objects.create(flat=flat,
                                                   field=value_key,
                                                   value=value)
        except Exception as ex:
            print ex

    def delete_building_objects(self):
        if not self.building:
            return
        try:
            bld = self.building
            BuildingFieldRecord.objects.filter(building=bld).delete()
            FlatFieldRecord.objects.filter(flat__building=bld).delete()
            FlatRecord.objects.filter(building=bld).delete()
        except Exception as ex:
            print ex
            return