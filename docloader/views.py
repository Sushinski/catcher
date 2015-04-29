from django.shortcuts import render
from docloader import fileloader
# Create your views here.


def upload_view(request):
    c = {'view': None, }
    return render(request, 'doc_upload_view.html', c)


def upload_result_view(request):
    wb = fileloader.Workbook(request.POST['upl_filename'])
    c = {'view': None, }
    return render(request, 'doc_upload_view.html', c)