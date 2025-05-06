from django.shortcuts import render, redirect
from user.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from history.models import History
from payment.models import Payment
from user.models import TransactionHistory
from django.utils.timezone import now
from decimal import Decimal
import json
# Create your views here.

# def index(request):
#     user = None
#     if 'user_id' in request.session:  # Kiểm tra session để xác định người dùng đã đăng nhập
#         try:
#             user = User.objects.get(id=request.session['user_id'])  # Lấy thông tin người dùng từ model tùy chỉnh
#         except User.DoesNotExist:
#             pass  # Nếu không tìm thấy user, bỏ qua
#     return render(request, 'app/index.html', {'user': user})  # Truyền thông tin người dùng vào template
def about_view(request):
    user = None
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass  # Không làm gì nếu không tìm thấy user

    return render(request, 'app/about.html', {'user': user})

def index(request):
    user = None
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass  # Không làm gì nếu không tìm thấy user

    return render(request, 'app/index.html', {'user': user})

def logout_view(request):
    #Xóa session để đăng xuất người dùng
    # if 'user_id' in request.session:
    #     del request.session['user_id']
    request.session.flush()  # 
    return redirect('index')


# def account_view(request):
#     user = None
#     user_id = request.session.get('user_id')
    
#     if user_id:
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             pass  # Không làm gì nếu không tìm thấy user

#     return render(request, 'app/account.html', {'user': user})

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

def account_view(request):
    user = None
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    transactions = TransactionHistory.objects.filter(user=user).order_by('-created_at') if user else []

    paginator = Paginator(transactions, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Nếu là request AJAX, trả về JSON chứa HTML của bảng và phân trang
        html = render_to_string('app/transaction_list.html', {
            'page_obj': page_obj,
        })
        return JsonResponse({'html': html})

    return render(request, 'app/account.html', {
        'user': user,
        'page_obj': page_obj,
    })


# View để xử lý nạp tiền (DEPOSIT)
def deposit_money(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount = Decimal(data.get('amount'))
            payment_method = data.get('payment_method')
            transaction_type = 'Nạp tiền'
            status = 'COMPLETED'

            

            with transaction.atomic():
                user = get_object_or_404(User.objects.select_for_update(), id=user_id)
                user.balance += amount
                user.save()

                transaction_history = TransactionHistory.objects.create(
                    user=user,
                    transaction_type=transaction_type,
                    amount=amount,
                    payment_method=payment_method,
                    status=status,
                    created_at=now()
                )

            return JsonResponse({
                'message': 'Nạp tiền thành công',
                'transaction_id': transaction_history.id,
                'amount': str(transaction_history.amount),
                'payment_method': transaction_history.payment_method,
                'new_balance': str(user.balance),
                
            }, status=201)

        except ValueError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)