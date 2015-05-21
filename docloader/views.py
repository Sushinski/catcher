# -*- coding: utf-8 -*-
from django.shortcuts import render
from docloader.fileloader import Workbook
from catcher.settings import UPLOAD_DIR
from models import CompanyRecord, FlatRecord


# todo ввод компания, этажность дома, адрес, район, срок сдачи, форма договора,  название комплекса, виды рассрочки,
# todo ипотека
wb = None
DOC_FIELDS = ('price', 'area', 'abs_area', 'district', 'rooms', 'floor', 'primary_fee', 'room_height',
              'kitchen_area', 'balcony')
DOC_RU_FIELDS = (u'Цена', u'Площадь', u'Общ. площадь', u'Район', u'Комнат', u'Этаж', u'Первый взнос', u'Потолок',
                 u'Пл. кухни', u'Балкон')
DOC_FIELDS_DICT = dict(zip(DOC_RU_FIELDS, DOC_FIELDS))

DOC_INPUT_FIELDS = [(u'company', u'Компания'), (u'house_floors', u'Этажность дома'), (u'address', u'Адрес'),
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


class UploadResultView():
    def __init__(self, filename):
        self.sheets = []  # страницы, содержащие headlines - заголовки
        self.sel_options = zip(DOC_FIELDS, DOC_RU_FIELDS)  # варианты целевых полей в базе
        self.single_fields = DOC_INPUT_FIELDS
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
        res = [(i, enumerate(sheet.row_values(i, 0, 25))) for i in range(sheet.nrows)]
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
        for sh in wb.sheets:  # for every table
            # 1st - get fields mapping
            started = False
            for i in range(sh.nrows):
                row = sh.row_values(i, 0, self.fields_num)
                row_1st_sel = request.POST[u'{0}_{1}'.format(sh.name, i)]
                if row_1st_sel == 'header':
                    self.get_field_fmt(request, sh.name, i, row)
                elif row_1st_sel == 'start_range' and self.fields_fmt:
                    self.save_rows_to_db(row, self.fields_fmt)
                    started = True
                elif row_1st_sel == 'end_range' and self.fields_fmt:
                    self.save_rows_to_db(row, self.fields_fmt)
                    started = False
                elif self.fields_fmt and started:
                    self.save_rows_to_db(row, self.fields_fmt)

    def get_field_fmt(self, request, sheet_name, row_num, row):
        res = dict()
        for i, fld in enumerate(row):
            value = request.POST[u'sel_{0}_{1}_{2}'.format(sheet_name, row_num, i)]
            res[value] = i
        self.fields_fmt = res

    def save_rows_to_db(self, row, fields):
        try:
            # company, created = \
            # CompanyRecord.objects.get_or_create(name=row[fields.get('company'])
            spr = [j for j in range(len(row)) if j not in fields.values()]
            rii = [unicode(row[k]) for k in spr if k != '']
            related_info = ','.join(rii)
            FlatRecord.objects.create(price=row[fields['price']],
                                      district=row[fields['district']],
                                      rooms=row[fields['rooms']],
                                      area=row[fields['area']],
                                      related_info=related_info)
        except Exception as ex:
            print ex