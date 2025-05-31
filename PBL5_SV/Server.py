from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import datetime, timezone, timedelta
import numpy as np
from mysql.connector import Error
from io import BytesIO
import threading
import cv2
import time
import os
import re
from werkzeug.utils import secure_filename


# Định nghĩa múi giờ UTC+7 (Hồ Chí Minh)
UTC_PLUS_7 = timezone(timedelta(hours=7))


UPLOAD_FOLDER = 'image_data/vehicle_images'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


from db import init_db_connection, get_db_connection

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

latest_frame = None

@app.route('/upload', methods=['POST'])
def upload_frame():
    global latest_frame
    if 'frame' not in request.files:
        return 'No frame received', 400

    file = request.files['frame']
    img_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    latest_frame = frame
    
    return 'Frame received', 200

@app.route('/video_feed', methods=['GET'])
def video_feed():
    def generate():
        global latest_frame
        while True:
            if latest_frame is not None:
                _, buffer = cv2.imencode('.jpg', latest_frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(0.05)
    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def verify_vehicle(license_plate):
    print(f"Verifying vehicle with license plate: {license_plate}")
    
    connection = get_db_connection()
    if connection is None or not connection.is_connected():
        return False, "Database connection error", None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT v.*, u.name as vehicle_owner 
            FROM vehicles v 
            LEFT JOIN users u ON v.user_id = u.id 
            WHERE v.license_plate = %s
        """
        cursor.execute(query, (license_plate,))
        vehicle = cursor.fetchone()
        cursor.close()

        if vehicle:
            return True, "Xe đã đăng ký", vehicle
        return False, "Xe chưa đăng ký", None

    except Error as e:
        return False, f"Database error: {e}", None


@app.route('/entrance_LPR', methods=['POST'])
def send_data_entrance():
    data = request.json
    license_plate = data.get('license_plate', '')
    current_time = datetime.now(UTC_PLUS_7)  # Sử dụng múi giờ UTC+7

    # Đầu tiên, lấy thông tin xe từ biển số
    is_registered, status_message, vehicle = verify_vehicle(license_plate)
    
    # Nếu xe không đăng ký, trả về thông báo
    if not is_registered:
        vehicle_info = {        
            'license_plate': license_plate,
            'status': 'Xe chưa đăng ký',
            'is_registered': False,
            'entry_time': current_time.strftime("%H:%M %d/%m/%Y"),
            'type': 'entrance'
        }
        
        socketio.emit('vehicle_info', vehicle_info)
        
        return jsonify({
            'status': 'Unregistered vehicle detected',
            'data': vehicle_info
        }), 200

    # Nếu xe đã đăng ký, tiếp tục xử lý
    vehicle_id = vehicle['id']  # Lấy id của xe từ kết quả verify_vehicle
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
          # Kiểm tra lần quét gần nhất của xe này (bất kể vào hay ra)
        last_scan_query = """
            SELECT time_in, time_out FROM histories 
            WHERE vehicle_id = %s
            ORDER BY COALESCE(time_out, time_in) DESC LIMIT 1
        """
        cursor.execute(last_scan_query, (vehicle_id,))
        last_scan = cursor.fetchone()
        
        # Nếu có lần quét gần đây, kiểm tra thời gian
        if last_scan:
            # Lấy thời gian gần nhất (time_out nếu có, nếu không thì time_in)
            last_time = last_scan['time_out'] if last_scan['time_out'] else last_scan['time_in']
            
            # Nếu last_time là naive datetime (không có thông tin múi giờ), thêm múi giờ UTC+7
            if last_time.tzinfo is None:
                last_time = last_time.replace(tzinfo=UTC_PLUS_7)
                
            time_diff = (current_time - last_time).total_seconds() / 60  # Phút
            
            # Nếu thời gian giữa hai lần quét < 1 phút, bỏ qua quét này
            if time_diff < 1:
                return jsonify({
                    'status': 'Ignored', 
                    'message': 'Same vehicle detected within 1 minute, ignoring...',
                    'license_plate': license_plate
                }), 200
        
        # Kiểm tra xem xe này đã có trong bãi đỗ chưa
        check_existing = """
            SELECT h.id, h.time_in, h.parking_space_id, p.space_number 
            FROM histories h
            LEFT JOIN parkingspace p ON h.parking_space_id = p.id
            WHERE h.vehicle_id = %s AND h.time_out IS NULL
            ORDER BY h.time_in DESC LIMIT 1
        """
        cursor.execute(check_existing, (vehicle_id,))
        existing_record = cursor.fetchone()
        
        # Nếu xe này đã có trong bãi đỗ (có bản ghi chưa có time_out), 
        # thì đây là xe đang ra
        if existing_record:
            # Cập nhật thời gian ra
            update_exit = """
                UPDATE histories 
                SET time_out = %s 
                WHERE id = %s
            """
            cursor.execute(update_exit, (current_time, existing_record['id']))
            
            # Cập nhật trạng thái chỗ đỗ xe dựa trên parking_space_id
            if existing_record['parking_space_id']:
                update_space = """
                    UPDATE parkingspace
                    SET is_occupied = 0 
                    WHERE id = %s
                """
                cursor.execute(update_space, (existing_record['parking_space_id'],))
                space_info = f"Chỗ đỗ {existing_record['space_number']} đã được giải phóng"
            else:
                # Fallback nếu không có parking_space_id
                update_space = """
                    UPDATE parkingspace
                    SET is_occupied = 0 
                    WHERE is_occupied = 1 
                    LIMIT 1
                """
                cursor.execute(update_space)
                space_info = "Một chỗ đỗ đã được giải phóng"
            
            connection.commit()
            
            # Tính thời gian đỗ xe
            time_in = existing_record['time_in']
            # Đảm bảo time_in có cùng múi giờ với current_time
            if time_in.tzinfo is None:
                time_in = time_in.replace(tzinfo=UTC_PLUS_7)
            
            parking_duration = round((current_time - time_in).total_seconds() / 3600, 1)  # Giờ đỗ xe
            
            # Tạo dữ liệu phản hồi cho xe ra
            vehicle_exit = {
                'license_plate': license_plate,
                'status': status_message,
                'is_registered': is_registered,
                'exit_time': current_time.strftime("%H:%M %d/%m/%Y"),
                'type': 'exit',
                'parking_duration': parking_duration,
                'space_info': space_info
            }
            
            if vehicle:
                vehicle_exit.update({
                    'vehicle_type': vehicle['vehicle_type'],
                    'user_id': vehicle['user_id'],
                    'vehicle_owner': vehicle['vehicle_owner']
                })
            
            socketio.emit('vehicle_exit', vehicle_exit)
            
            return jsonify({
                'status': 'Vehicle exit processed successfully',
                'data': vehicle_exit
            }), 200
            
        else:
            # Đây là xe đang vào
            # Tìm một chỗ đỗ xe trống
            find_empty_space = """
                SELECT id, space_number, level
                FROM parkingspace 
                WHERE is_occupied = 0 
                LIMIT 1
            """
            cursor.execute(find_empty_space)
            empty_space = cursor.fetchone()
            
            if empty_space:
                # Cập nhật chỗ đỗ thành đã có xe
                update_space = """
                    UPDATE parkingspace 
                    SET is_occupied = 1 
                    WHERE id = %s
                """
                cursor.execute(update_space, (empty_space['id'],))
                
                # Thêm vào lịch sử với parking_space_id
                insert_history = """
                    INSERT INTO histories (vehicle_id, time_in, parking_space_id)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_history, (vehicle_id, current_time, empty_space['id']))
                
                space_info = f"Sẽ đỗ tại chỗ {empty_space['space_number']} - Tầng {empty_space['level']}"
            else:
                # Nếu không tìm thấy chỗ đỗ trống
                insert_history = """
                    INSERT INTO histories (vehicle_id, time_in)
                    VALUES (%s, %s)
                """
                cursor.execute(insert_history, (vehicle_id, current_time))
                space_info = "Không tìm thấy chỗ đỗ trống"
            
            connection.commit()
            
            # Tạo dữ liệu phản hồi cho xe vào
            vehicle_info = {        
                'license_plate': license_plate,
                'status': status_message,
                'is_registered': is_registered,
                'entry_time': current_time.strftime("%H:%M %d/%m/%Y"),
                'type': 'entrance',
                'space_info': space_info
            }

            vehicle_info.update({
                'vehicle_type': vehicle['vehicle_type'],
                'user_id': vehicle['user_id'],
                'vehicle_owner': vehicle['vehicle_owner']
            })

            socketio.emit('vehicle_info', vehicle_info)
            
            return jsonify({
                'status': 'Vehicle entry processed successfully',
                'data': vehicle_info
            }), 200

    except Error as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@socketio.on('connect')
def handle_connect():
    print("✅ A client connected!")


if __name__ == '__main__':
    init_db_connection()  # Kết nối duy nhất tại đây
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
