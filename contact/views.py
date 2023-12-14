from django.shortcuts import render, redirect
from .forms import ApplicationForm, SMSVerificationForm
from .models import ApplicationCreate, HujumTuri, Application, Tuman
import http.client
import random
from django.conf import settings
import os
from PIL import Image, ImageDraw, ImageFont
import string
from django.http import HttpResponse
from io import BytesIO


def index(request):
    ariza_son = ApplicationCreate.objects.count()
    tasdiq_ariza = ApplicationCreate.objects.filter(status=3).count()
    notasdiq_ariza = ariza_son - tasdiq_ariza
    query = HujumTuri.objects.all()
    ctx = {'query': query, 'ariza_son': ariza_son, 'tasdiq_ariza': tasdiq_ariza, 'notasdiq_ariza': notasdiq_ariza}
    return render(request, 'users/index.html', ctx)


def send_sms_to_user(phone_number, sms_code):
    url = settings.BASE_URL
    token = settings.API_KEY
    SENDER = settings.SENDER
    RECIPIENT = f"{phone_number}"
    MESSAGE_TEXT = f"Sizni arizani tasdiqlash kodingiz: {sms_code}"

    conn = http.client.HTTPSConnection(url)

    payload1 = "{\"messages\":" \
               "[{\"from\":\"" + SENDER + "\"" \
                                          ",\"destinations\":" \
                                          "[{\"to\":\"" + RECIPIENT + "\"}]," \
                                                                      "\"text\":\"" + MESSAGE_TEXT + "\"}]}"

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload1, headers)


def serialize_tuman(tuman):
    return str(tuman)


# HujumTuri modelida __str__ usuli yoki uni satr sifatida ko'rsatishning boshqa usuli mavjud deb hisoblasakg
def serialize_hujum_turi(hujum_turi):
    return str(hujum_turi)


def ariza(request):
    if request.method == 'POST':
        forms = ApplicationForm(request.POST, request.FILES)
        if forms.is_valid():
            sms_code = str(random.randint(100000, 999999))
            send_sms_to_user(request.POST['phone'], sms_code)
            print(sms_code)

            # Convert date objects to strings
            application_data = forms.cleaned_data
            application_data['birthday'] = application_data.get('birthday', None).strftime(
                '%Y-%m-%d') if application_data.get('birthday') else None
            application_data['vaqt'] = application_data.get('vaqt', None).strftime(
                '%Y-%m-%d %H:%M:%S') if application_data.get('vaqt') else None

            # Convert Tuman object to a serializable format
            district = application_data.get('district')
            application_data['district'] = str(district) if district else None

            # Convert HujumTuri object to a serializable format
            hujum_turi = application_data.get('hujumturi')
            application_data['hujumturi'] = str(hujum_turi) if hujum_turi else None

            # Handle file upload separately
            uploaded_file = request.FILES.get('rasm')
            if uploaded_file:
                # Save the file to the server and store its path or identifier in the session
                file_path = save_uploaded_file(uploaded_file)
                application_data['rasm'] = file_path

            request.session['application_data'] = application_data
            request.session['application_data']['sms_code'] = sms_code
            print(forms.errors)
            return redirect('verify_sms_code')
    else:
        forms = ApplicationForm()
    context = {'forms': forms}
    return render(request, 'users/form.html', context)


def save_uploaded_file(uploaded_file):
    # Specify the base directory path to save uploaded files
    base_directory = os.path.join(settings.MEDIA_ROOT, 'chek_rasm')

    # Specify the subdirectory (e.g., 'img')
    save_directory = os.path.join(base_directory)

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Save the file to a designated location on the server
    file_path = os.path.join(save_directory, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    # Return the relative path, which can be used as the file URL
    relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT)
    return relative_path


# def verify_sms_code(request):
#     if request.method == 'POST':
#         sms_verification_form = SMSVerificationForm(request.POST)
#         application_data = request.session.get('application_data')
#         kod = application_data['sms_code']
#         xato_soni = request.session.get('xato_soni', 0)
#
#         if sms_verification_form.is_valid():
#             if application_data and request.POST['sms_code'] == kod:
#                 application_data.pop('sms_code', None)
#                 tuman_name = application_data.get('district')
#                 district, created = Tuman.objects.get_or_create(tuman_name=tuman_name)
#                 application_data['district'] = district
#                 hujumturi_name = application_data.get('hujumturi')
#                 hujumturi, created = HujumTuri.objects.get_or_create(hujum_name=hujumturi_name)
#                 application_data['hujumturi'] = hujumturi
#                 Application.objects.create(**application_data)
#                 request.session.pop('application_data')
#                 request.session.pop('xato_soni')
#                 return redirect('index')
#         else:
#             xato_soni += 1
#             request.session['xato_soni'] = xato_soni
#             if xato_soni >= 2:
#                 request.session['captcha_required'] = True
#
#     sms_verification_form = SMSVerificationForm()
#     application_data = request.session.get('application_data')
#     kod = application_data['sms_code']
#     context = {'sms_verification_form': sms_verification_form, 'kod': kod}
#     return render(request, 'users/smsCode.html', context)

# def generate_captcha_image(request):
#     width, height = 150, 50
#     image = Image.new("RGB", (width, height), (73, 255, 255))
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.load_default()
#     captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
#     request.session['captcha_text'] = captcha_text
#     response = HttpResponse(content_type="image/png")
#     image.save(response, "PNG")
#     return response

def verify_sms_code(request):
    if request.method == 'POST':
        sms_verification_form = SMSVerificationForm(request.POST)
        application_data = request.session.get('application_data')
        kod = application_data['sms_code']
        if sms_verification_form.is_valid():
            print('sms kod', kod)
            if application_data and request.POST['sms_code'] == kod:
                # Remove 'sms_code' key before creating the Application instance
                application_data.pop('sms_code', None)

                # Get or create the Tuman instance based on the district name
                tuman_name = application_data.get('district')
                district, created = Tuman.objects.get_or_create(tuman_name=tuman_name)

                # Replace the district string with the Tuman instance
                application_data['district'] = district

                # Get or create the HujumTuri instance based on the hujumturi name
                hujumturi_name = application_data.get('hujumturi')
                hujumturi, created = HujumTuri.objects.get_or_create(hujum_name=hujumturi_name)

                # Replace the hujumturi string with the HujumTuri instance
                application_data['hujumturi'] = hujumturi

                # Save user information to the database
                Application.objects.create(**application_data)

                request.session.pop('application_data')

                return redirect('index')
    else:
        sms_verification_form = SMSVerificationForm()
        application_data = request.session.get('application_data')
        kod = application_data['sms_code']
    context = {'sms_verification_form': sms_verification_form, 'kod': kod}
    return render(request, 'users/smsCode.html', context)


# def generate_captcha_image(request):
#     width, height = 150, 50
#     image = Image.new("RGB", (width, height), (255, 255, 255))
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.load_default()
#     captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
#
#     # Save the captcha text to the session for later verification
#     request.session['captcha_text'] = captcha_text
#
#     # Convert the image to PNG and return as response
#     response = HttpResponse(content_type="image/png")
#     image.save(response, "PNG")
#     return response

def handle_uploaded_file(uploaded_file):
    # Fayl nomi va joylashuvi
    file_name = uploaded_file.name
    file_path = f"uploads/{file_name}"

    # Tekshirish
    if default_storage.exists(file_path):
        return HttpResponseBadRequest('Bu nomda fayl allaqachon mavjud.')

    # Faylni serverga yuklab olish
    with default_storage.open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path