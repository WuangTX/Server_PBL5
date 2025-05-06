from django.shortcuts import render
from django.http import JsonResponse
from user.models import User  # Import bảng User
from django.contrib.auth.hashers import check_password  # Để kiểm tra mật khẩu đã hash

def login_view(request):

    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Tìm user theo email
            user = User.objects.get(email=email)
            
            # Kiểm tra mật khẩu
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return JsonResponse({'status': 'success', 'message': 'Đăng nhập thành công!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Email hoặc mật khẩu không đúng!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Người dùng không tồn tại!'})
        
    context = {
        'user': user,
    }

    return render(request, 'login/login.html', context)
