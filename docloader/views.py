from django.shortcuts import render
from docloader import fileloader
from catcher.settings import UPLOAD_DIR
from models import CompanyRecord, FlatRecord

wb = None
DOC_FIELDS = ('price', 'area', 'district', 'rooms')


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
        global wb
        wb = fileloader.Workbook(filename)
        self.rows = zip(enumerate(wb.sheet_names()), wb.dimensions())


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
        rows = zip(enumerate(wb.sheet_names()), wb.dimensions())
        for r in rows:
            dest_row_range_str = request.POST['range%d' % r[0][0]]
            dest_fields_str = request.POST['map%d' % r[0][0]]
            if len(dest_row_range_str) and len(dest_fields_str):
                dest_row_range_list = [tuple(elem.strip(' ').split('-')) for elem in dest_row_range_str.split(',')]
                dest_fields_list = [fld.strip('()').replace('\n', ' ') for fld in dest_fields_str.split('),(')]
                fld_index_dict = self.get_indexes_dict(r[0][0], dest_fields_list)
                for x, y in dest_row_range_list:
                    self.save_rows_to_db(r[0][0], int(x), int(y), fld_index_dict)

    def save_rows_to_db(self, sheet_no, row_from, row_to, fields):
        print row_from, row_to
        try:
            sh = self.wb.get_sheet(sheet_no)
            for i in range(row_from, row_to):
                row = sh.row_values(i)
                # company, created = \
                #    CompanyRecord.objects.get_or_create(name=row[fields.get('company'])
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

    def get_indexes_dict(self, sheet_no, field_names):
        res = dict()
        try:
            sh = self.wb.get_sheet(sheet_no)
            idx = 0
            fld_nams_enum = [(key, value) for value, key in enumerate(field_names)]
            fld_names_dict = dict(fld_nams_enum)
            for i in range(sh.nrows):
                vals = [unicode(elem).replace('\n', ' ') for elem in sh.row_values(i)]
                for j, fld in enumerate(vals):
                    if fld in field_names:
                        index = fld_names_dict[fld]
                        res[DOC_FIELDS[index]] = j
                        idx += 1
                        if idx == len(DOC_FIELDS):
                            return res
            return None
        except Exception as ex:
            print ex
            return None