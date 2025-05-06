from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user.models import User
from user.models import Vehicle
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# @csrf_exempt
def register_view(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    #vehicles = Vehicle.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        
        #print(full_name, email, phone, password, license_plate, vehicle_type, vehicle_image)
          # Kiểm tra email đã tồn tại
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

         # Save user to database
        user = User.objects.create(
            name=full_name,
            email=email,
            phone_number=phone,
            password=make_password(password)  # Hash the password
        )
        return JsonResponse({'message': 'Registration successful'})
    # return render(request, 'register/register.html', {'vehicles': vehicles, 'MEDIA_URL': settings.MEDIA_URL})
    context = {
        'user': user,
    }
    return render(request, 'register/registerUser.html',context)


def register_vehicle(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        license_plate = request.POST.get('license_plate')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_image = request.FILES.get('vehicle_image')

        # Kiểm tra biển số xe đã tồn tại chưa
        if Vehicle.objects.filter(license_plate=license_plate).exists():
            return JsonResponse({'error': 'Biển số xe đã tồn tại'}, status=400)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        vehicle_image_url = fs.save(vehicle_image.name, vehicle_image)

        vehicle = Vehicle.objects.create(
            license_plate=license_plate,
            vehicle_type=vehicle_type,
            image_path=vehicle_image_url,
            user=user
        )
        
        return JsonResponse({'message': 'Đăng ký xe thành công'})
    
    context = {'user': user}
    return render(request, 'register/registerVehicle.html', context)