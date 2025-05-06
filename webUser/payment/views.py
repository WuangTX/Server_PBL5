# from django.shortcuts import render
# from user.models import User

# # Create your views here.
# def payment_view(request):
#     user = None
#     user_id = request.session.get('user_id')
#     if user_id:
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             pass

#     context = {
#         'user': user,
#     }
#     return render(request, 'payment/payment.html',context)

from django.shortcuts import render
from user.models import User
from history.models import History
from payment.models import Payment
from user.models import TransactionHistory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.utils.timezone import now
import json

def payment_view(request):
    user = None
    unpaid_histories = []

    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)

            # Lọc các lịch sử của user có payment và status=False
            unpaid_histories = History.objects.filter(
                vehicle__user=user,
                payment__status=False
            ).select_related('vehicle', 'payment')

        except User.DoesNotExist:
            pass

    context = {
        'user': user,
        'unpaid_histories': unpaid_histories,
    }
    return render(request, 'payment/payment.html', context)


from django.http import JsonResponse
from history.models import History

def vehicle_details_api(request):
    history_id = request.GET.get('history_id')
    if not history_id:
        return JsonResponse({'error': 'Missing history_id'}, status=400)

    try:
        history = History.objects.select_related('vehicle').get(id=history_id)

        hours, minutes = history.get_parking_duration()
        fee = history.calculate_fee()

        return JsonResponse({
            'plateNumber': history.vehicle.license_plate,
            'entryTime': history.time_in.strftime('%d-%m-%Y %H:%M:%S'),
            'exitTime': history.time_out.strftime('%d-%m-%Y %H:%M:%S') if history.time_out else 'Chưa xác định',
            'parkingDuration': f"{hours} giờ {minutes} phút",
            'totalFee': fee
        })

    except History.DoesNotExist:
        return JsonResponse({'error': 'History not found'}, status=404)

# View để xử lý thanh toán phí gửi xe (PAYMENT)
def process_parking_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history_id = data.get('history_id')
            payment_method = data.get('payment_method')
            transaction_type = 'Phí gửi xe'
            status = 'COMPLETED'

           

            history = get_object_or_404(History, id=history_id)

            

            # Lấy Payment tương ứng với History
            payment = Payment.objects.filter(history=history).first()
            if not payment:
                return JsonResponse({'error': 'Không tìm thấy thông tin thanh toán cho lịch sử này'}, status=404)
            
             # Kiểm tra nếu Payment đã được thanh toán
            if payment.status:
                return JsonResponse({'error': 'Lịch sử này đã được thanh toán trước đó'}, status=400)
            
            fee = payment.fee
           

            with transaction.atomic():
                user = get_object_or_404(User.objects.select_for_update(), id=history.vehicle.user.id)
                if user.balance < fee:
                    return JsonResponse({'error': 'Số dư không đủ để thanh toán'}, status=400)

                user.balance -= fee
                user.save()

                # Cập nhật trạng thái Payment
                payment.status = True
                payment.created_at = now()
                payment.save()

                transaction_history = TransactionHistory.objects.create(
                    user=user,
                    transaction_type=transaction_type,
                    amount=-fee,
                    payment_method=payment_method,
                    status=status,
                    payment=payment,
                    created_at=now()
                )

            return JsonResponse({
                'message': 'Thanh toán phí gửi xe thành công',
                'transaction_id': transaction_history.id,
                'amount': str(transaction_history.amount),
                'payment_method': transaction_history.payment_method,
                'new_balance': str(user.balance),
                'payment_id': payment.id,
                'created_at': transaction_history.created_at.isoformat()
            }, status=201)

        except ValueError:
            return JsonResponse({'error': 'Dữ liệu không hợp lệ'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)
