from django.shortcuts import render
from contact.models import Application, ApplicationCreate, Tuman, HujumTuri
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from .views import login_decorator
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side

@login_decorator
def tablitsa(request):
    application = Application.objects.select_related('hujumturi', 'district', 'app_create').all()

    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    hujumturi_id = request.GET.get('hujum', '')
    district_id = request.GET.get('tuman', '')
    status = request.GET.get('status', '')

    if first_name:
        application = application.filter(first_name__icontains=first_name)
    if last_name:
        application = application.filter(last_name__icontains=last_name)
    if district_id:
        application = application.filter(district_id=district_id)
    if status:
        application = application.filter(app_create__status=status)  # Adjusted filter here
    if hujumturi_id:
        application = application.filter(hujumturi_id=hujumturi_id)

    tumans = Tuman.objects.all()
    status_choices = ApplicationCreate.STATUS_CHOICES
    hujumturi = HujumTuri.objects.all()

    paginator = Paginator(application, 6)
    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    ctx = {'applications': applications, 'tumans': tumans, 'status_choices': status_choices, 'hujumturi': hujumturi}
    return render(request, 'dashboard/tablitsa.html', ctx)


@login_decorator
def export_to_excel(request):
    # Olingan arizalar
    applications = Application.objects.select_related('hujumturi', 'district', 'app_create').all()

    wb = Workbook()
    ws = wb.active

    # Styles
    header_style = Font(bold=True, color='FFFFFF')
    cell_style = Alignment(horizontal='left', vertical='center')
    header_fill = PatternFill(start_color='0072BA', end_color='0072BA', fill_type='solid')

    # Header row
    header_row = ['F.I.Sh', 'Telefon', 'Tug\'ilgan yili', 'Passport', 'Tuman', 'Manzil', 'jins', 'Hujum turi',
                  'Plastik raqami', 'Plastik raqami \ngumondor', 'Gumondor F.I.Sh', 'Gumondor \n telefon raqami',
                  'Pul yechilgan \nsana', 'Pul yechib \nolingan summa', 'Shaxs ishlatgan\n ilova',
                  'Gumondor\n ishlatgan ilova', 'Shaxs yozgan\n qisqa so\'z', 'Status']
    for col_num, value in enumerate(header_row, 1):
        col_letter = get_column_letter(col_num)
        ws[f'{col_letter}1'] = value
        ws[f'{col_letter}1'].font = header_style
        ws[f'{col_letter}1'].alignment = cell_style
        ws[f'{col_letter}1'].fill = header_fill

    # Data rows
    for row_num, app in enumerate(applications, 2):
        ws[f'A{row_num}'] = f'{app.first_name} {app.last_name} {app.surname}'
        ws[f'B{row_num}'] = app.phone
        ws[f'C{row_num}'] = app.birthday
        ws[f'D{row_num}'] = app.passport_serial
        ws[f'E{row_num}'] = app.district.tuman_name if app.district else ''
        ws[f'F{row_num}'] = app.address
        ws[f'G{row_num}'] = app.gender
        ws[f'H{row_num}'] = app.hujumturi.hujum_name if app.hujumturi else ''
        ws[f'I{row_num}'] = app.plastikraqam_ozi
        ws[f'J{row_num}'] = app.plastikraqam_gumondor
        ws[f'K{row_num}'] = app.full_name_gumondor
        ws[f'L{row_num}'] = app.phone_gumondor
        ws[f'M{row_num}'] = app.vaqt
        ws[f'N{row_num}'] = app.summa
        ws[f'O{row_num}'] = app.ilova
        ws[f'P{row_num}'] = app.ilova_gumondor
        ws[f'Q{row_num}'] = app.text
        ws[f'R{row_num}'] = app.app_create.status if app.app_create else ''

    # Apply borders to all cells
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.border = Border(left=Side(style='thin', color='000000'),
                                 right=Side(style='thin', color='000000'),
                                 top=Side(style='thin', color='000000'),
                                 bottom=Side(style='thin', color='000000'))

    # Excel faylini HTTP javob qilib qaytarish
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=arizalar.xlsx'
    response.write(save_virtual_workbook(wb))

    return response