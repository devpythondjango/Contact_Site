# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ApplicationForm
from .models import ApplicationCreate
import http.client
import random
from django.conf import settings

def index(request):
    return render(request, 'users/index.html')

# Bu yerda serverda saqlanadigan sms_code ni belgilash uchun o'zgaruvchi
server_generated_sms_code = None

def send_sms(request):
    global server_generated_sms_code
    if request.method == 'POST':
        data = request.POST
        phone = data.get('phone')
        sms_code = data.get('smsCode')
        print('tel', phone)
        # send_sms_to_user(phone)
        # Bu joyda sms_code ni to'g'ri tekshirishni bajarishingiz kerak
        if sms_code == server_generated_sms_code:
            server_generated_sms_code = None  # Solishtirilgandan so'ng o'zgaruvchini tozalash
            return JsonResponse({'success': True})
        else:
            # SMS kodi xato
            return JsonResponse({'success': False, 'error': 'Invalid SMS code'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def ariza(request):
    global server_generated_sms_code
    if request.method == 'POST':
        forms = ApplicationForm(request.POST, request.FILES)
        response = send_sms(request)
        data = request.POST
        phone = data.get('phone')
        print(phone)
        # send_sms_to_user(phone)
        if response.get('success', True):
            if forms.is_valid():                
                try:
                    application_instance = forms.save()
                    application_create_instance = ApplicationCreate.objects.create(application=application_instance)
                    return redirect('index')
                except Exception as e:
                    print(f"Formani saqlashda xatolik yuzaga keldi: {e}")
                    return JsonResponse({'success': False, 'error': 'Ma\'lumotlarni saqlashda xatolik'})

            else:
                return JsonResponse({'success': False, 'error': 'Invalid form data'})

    else:
        forms = ApplicationForm()

    server_generated_sms_code = str(random.randint(100000, 999999))
    print('post sms', server_generated_sms_code)

    context = {'forms': forms, 'server_generated_sms_code': server_generated_sms_code}
    return render(request, 'users/form.html', context)

def send_sms_to_user(phone_number):
    sms_code = server_generated_sms_code
    print('tel sms', sms_code) 
    # Twilio ma'lumotlari
    url = settings.BASE_URL
    token = settings.API_KEY
    SENDER = "PYTHON"
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

    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))