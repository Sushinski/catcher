from django.shortcuts import render
from docloader import fileloader
from catcher.settings import UPLOAD_DIR
# Create your views here.


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
    name = UPLOAD_DIR+str(f)
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
        wb = fileloader.Workbook(filename)
        self.rows = zip(enumerate(wb.sheet_names(), 1), wb.dimensions())



