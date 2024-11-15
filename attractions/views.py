from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from datetime import datetime
from django.db import connection
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
import time
# 主页面展示
@login_required
def view_attractions(request):
    # 获取省份列表（包含英文名和中文名）
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, zh_name FROM attractions_province")
        provinces = cursor.fetchall()

    # 获取选定省份
    selected_province = request.GET.get('province', provinces[0][0] if provinces else None)

    # 获取选定省份的景点
    attractions = []
    if selected_province:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    attractions_attraction.id, 
                    attractions_attraction.name, 
                    attractions_attraction.description, 
                    attractions_attraction.location, 
                    attractions_attraction.image,
                    attractions_attraction.total_price
                FROM attractions_attraction
                JOIN attractions_province
                    ON attractions_attraction.province_name_id = attractions_province.name
                WHERE attractions_province.id = %s
            """, [selected_province])
            attractions = cursor.fetchall()

    # 获取选中景点的详细信息
    selected_attraction = None
    attraction_id = request.GET.get('attraction_id')
    if attraction_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    id, name, description, location, image, total_price
                FROM attractions_attraction
                WHERE id = %s
            """, [attraction_id])
            selected_attraction = cursor.fetchone()

    # 格式化省份列表（包含中文名和英文名）
    provinces_list = [
        {'id': province[0], 'name': province[1], 'zh_name': province[2]}  # 提供中文名 zh_name 和英文名 name
        for province in provinces
    ]

    return render(request, 'view_attractions.html', {
        'provinces': provinces_list,
        'attractions': attractions,
        'selected_province': selected_province,
        'selected_attraction': selected_attraction,
        'attraction_id': attraction_id,
    })


# 处理提交评论的视图函数
def submit_review(request, attraction_id):
    print("afdjiksadhgnfkmlg,hfdfs")
    if request.method == 'POST':
        try:
            attraction = get_object_or_404(Attraction, id=attraction_id)
            print(attraction)
            rating = request.POST.get('rating')
            print(rating)
            comment = request.POST.get('comment')
            print(request.user.username)

            # 创建评论
            review = Review.objects.create(
                attraction=attraction,
                rating=rating,
                comment=comment,
                name=request.user,  # 假设用户已登录
            )
            print("creat success")
            return JsonResponse({'success': True, 'message': '评论提交成功！'})

        except IntegrityError as e:
            return JsonResponse({'success': False, 'message': '数据库错误: ' + str(e)}, status=500)

        except Exception as e:
            return JsonResponse({'success': False, 'message': '服务器错误: ' + str(e)}, status=500)

    return JsonResponse({'success': False, 'message': '无效的请求方式。'}, status=400)


# 获取某省的景点列表
def get_attractions_by_province(request, province_name):
    try:
        # 查询数据库中的景点数据
        with connection.cursor() as cursor:
            # 定义查询语句，使用 INNER JOIN 连接 attractions_attraction 和 province 表
            # 假设 attractions_attraction 表有 province_name 字段
            SELECT = """
            SELECT attractions_attraction.id, attractions_attraction.name, attractions_attraction.image,attractions_attraction.description,attractions_attraction.location,attractions_attraction.total_price
            FROM attractions_attraction
            INNER JOIN attractions_province ON attractions_attraction.province_name_id = attractions_province.name
            WHERE attractions_province.name = %s
            """
            cursor.execute(SELECT, [province_name])

            # 获取查询结果
            rows = cursor.fetchall()

        # 处理查询结果
        attraction_data = [
            {
                "id": row[0],
                "name": row[1],
                "image_url": row[2] if row[2] else "",
                "description" : row[3],
                "location" : row[4],
                "total_price" : row[5]
            } for row in rows
        ]

        return JsonResponse({"attractions": attraction_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




# 获取景点详情
def get_attraction_detail(request, attraction_id):
    with connection.cursor() as cursor:
        select = """
                SELECT id, name, description, image, location, total_price
                FROM attractions_attraction
                WHERE id = %s
                """
        cursor.execute(select, [attraction_id])
        row = cursor.fetchone()
    reviews = []
    # 如果没有找到对应的景点
    if not row:
        attraction_data = {
            'id': 0,
            'name': '没有此景点',
            'description': '没有此景点',
            'image_url':  'https://bkimg.cdn.bcebos.com/pic/472309f790529822720e9e9844856ccb0a46f21f7e12?x-bce-process=image/format,f_auto/resize,m_lfit,limit_1,h_300',
            # 如果图片存在则返回图片路径
            'location': '没有此景点',
            'total_price': 0,
            'reviews': reviews
        }

    else:
        if attraction_id:
            with connection.cursor() as cursor:
                select ="""
                        SELECT users_user.username,rating,comment,created_at
                        FROM attractions_review
                        JOIN users_user ON attractions_review.name_id = users_user.username
                        WHERE attraction_id = %s
                        ORDER BY created_at DESC
                    """
                cursor.execute(select, [attraction_id])
                reviews = cursor.fetchall()
    # 构造返回的数据
        attraction_data = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'image_url': row[3] if row[3] else 'https://bkimg.cdn.bcebos.com/pic/472309f790529822720e9e9844856ccb0a46f21f7e12?x-bce-process=image/format,f_auto/resize,m_lfit,limit_1,h_300',  # 如果图片存在则返回图片路径
            'location': row[4],
            'total_price': row[5],
            'reviews': reviews
        }
    return JsonResponse({'attraction': attraction_data})


# 景点预定
@login_required
def reservation(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)

    if request.method == 'POST':
        # 获取表单数据
        date = request.POST['date']
        time = request.POST['time']
        num_people = request.POST['num_people']
        total_price = float(num_people) * attraction.total_price  # 计算总价
        contact_name = request.POST['contact_name']
        contact_phone = request.POST['contact_phone']
        note = request.POST.get('note', '')

        # 创建预约记录
        reservation = Reservation.objects.create(
            user=request.user,
            attraction=attraction,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time=time,
            num_people=num_people,
            total_price=total_price,
            contact_name=contact_name,
            contact_phone=contact_phone,
            note=note
        )

        # 提交成功后跳转到预约详情页面（或可以自定义跳转的页面）
        return redirect('reservation_success', reservation_id=reservation.id)

    return render(request, 'reservation.html', {
        'attraction': attraction
    })


@login_required
def reservation_success(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_success.html', {
        'reservation': reservation
    })

@login_required
def profile_view(request):
    user_id = request.user.id
    user_name = request.user.username
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        # 使用 SQL 更新用户信息
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE users_user
                    SET username = %s, email = %s, gender = %s, phone = %s
                    WHERE id = %s
                """, [username, email, gender, phone, user_id])

            return JsonResponse({'success': True})  # 返回 JSON 响应，表示更新成功
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})  # 返回失败信息
    else:
        # 使用 SQL 查询用户信息
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT username, last_login, email, date_joined, gender, phone, role
                FROM users_user
                WHERE id = %s
            """, [user_id])
            user_data = cursor.fetchone()

        # 检查是否成功获取数据
        if user_data:
            user_info = {
                'username': user_data[0],
                'last_login': user_data[1],
                'email': user_data[2],
                'date_joined': user_data[3],
                'gender': user_data[4],
                'phone': user_data[5],
                'role': user_data[6],
            }
        else:
            user_info = None
        # 查询用户的评论数据
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT attractions_review.attraction_id, attractions_attraction.name AS attraction_name, 
                       attractions_review.rating, attractions_review.comment, attractions_review.created_at
                FROM attractions_review
                JOIN attractions_attraction ON attractions_review.attraction_id = attractions_attraction.id
                WHERE attractions_review.name_id = %s
            """, [user_name])
            reviews = cursor.fetchall()

        # 将评论数据转为字典格式
        if reviews:
            reviews_data = [
                {
                    'attraction_id': review[0],
                    'attraction_name': review[1],  # 景点名称字段
                    'rating': review[2],
                    'comment': review[3],
                    'created_at': review[4],
                }
                for review in reviews
            ]
        else:
            reviews_data = []  # 如果查询结果为空，定义 reviews_data 为空列表

        return render(request, 'profile.html', {'user_info': user_info, 'reviews': reviews_data})

@login_required
def my_reservations_view(request):
    user_id = request.user.id

    # SQL 查询已支付的预约
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT r.id, r.attraction_id, r.date, r.time, r.num_people, 
                       r.total_price, r.contact_name, r.contact_phone, r.note, 
                       r.created_at,r.status ,a.image,a.name
                FROM attractions_reservation AS r
                JOIN attractions_attraction AS a ON r.attraction_id = a.id
                WHERE r.user_id = %s AND r.is_paid = 1
                ORDER BY r.date DESC
            """, [user_id])
        paid_reservations_raw = cursor.fetchall()

    paid_reservations = [
        {
            "id": row[0],
            "attraction_id": row[1],
            "date": row[2],
            "time": row[3],
            "num_people": row[4],
            "total_price": row[5],
            "contact_name": row[6],
            "contact_phone": row[7],
            "note": row[8],
            "created_at": row[9],
            'image': row[11],
            'name':row[12],
            'status':row[10]
        }
        for row in paid_reservations_raw
    ]
    print(paid_reservations)
    # 查询未支付的预约
    with connection.cursor() as cursor:
        cursor.execute("""
                 SELECT r.id, r.attraction_id, r.date, r.time, r.num_people, 
                        r.total_price, r.contact_name, r.contact_phone, r.note, 
                        r.created_at, a.image,a.name
                 FROM attractions_reservation AS r
                 JOIN attractions_attraction AS a ON r.attraction_id = a.id
                 WHERE r.user_id = %s AND r.is_paid = 0
                 ORDER BY r.date DESC
             """, [user_id])
        unpaid_reservations_raw = cursor.fetchall()
    unpaid_reservations = [
        {
            "id": row[0],
            "attraction_id": row[1],
            "date": row[2],
            "time": row[3],
            "num_people": row[4],
            "total_price": row[5],
            "contact_name": row[6],
            "contact_phone": row[7],
            "note": row[8],
            "created_at": row[9],
            'image': row[10],
            'name': row[11]
        }
        for row in unpaid_reservations_raw
    ]
    print(paid_reservations)
    return render(request, 'my_reservations.html', {
        'paid_reservations': paid_reservations,
        'unpaid_reservations': unpaid_reservations,
    })

@login_required
def pay_reservation(request, reservation_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attractions_reservation
            SET is_paid = TRUE, payment_date = %s
            WHERE id = %s
        """, [timezone.now(), reservation_id])
    return redirect('payment_success')

@login_required
def pay_all_reservations(request):
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attractions_reservation
            SET is_paid = TRUE, payment_date = %s
            WHERE user_id = %s AND is_paid = FALSE
        """, [timezone.now(), user_id])
    return redirect('payment_success')

def payment_success(request):
    return render(request, 'payment_success.html')

# 管理所有景点
@staff_member_required
def manage_all_attractions(request):
    attractions = Attraction.objects.all()
    return render(request, 'manage_all_attractions.html', {'attractions': attractions})


# 判断是否为景区管理员或总管理员
def manager_required(user):
    return user.role == 'attraction_manager'


@login_required
@user_passes_test(manager_required)
def manager_dashboard(request):
    user_id = request.user.id
    # 获取景区管理员管理的景点
    managed_attractions = Attraction.objects.filter(manager_id=user_id)
    approved_reservations = []
    rejected_reservations = []
    upcoming_reservations = []
    next_month_count = 0
    daily_reservations = {}  # 用于存储每天的预约人数
    # reservations_dict = {}
    for attraction in managed_attractions:
        with connection.cursor() as cursor:
            # 获取未来一个月的预约数量
            cursor.execute("""
                SELECT COUNT(*)
                FROM attractions_reservation
                WHERE attraction_id = %s AND is_paid = 1 AND date >= CURRENT_DATE AND date < date(CURRENT_DATE, '+1 month')
            """, [attraction.id])
            next_month_count += cursor.fetchone()[0]

            # 获取近一个月每天的预约人数
            cursor.execute("""
                            SELECT date, COUNT(*)
                            FROM attractions_reservation
                            WHERE attraction_id = %s AND is_paid = 1 AND date >= CURRENT_DATE AND date < date(CURRENT_DATE, '+1 month')
                            GROUP BY date
                            ORDER BY date
                        """, [attraction.id])

            daily_reservations_data = cursor.fetchall()
            for date, count in daily_reservations_data:
                # 将每天的预约人数添加到字典中
                daily_reservations[str(date)] = count

            # 获取已支付、待管理员同意或拒绝的预约
            cursor.execute("""
                SELECT r.id, r.user_id, r.contact_name, r.contact_phone, r.note, r.created_at, r.status, a.name AS attraction_name
                FROM attractions_reservation AS r
                JOIN attractions_attraction AS a ON r.attraction_id = a.id
                WHERE r.attraction_id = %s AND r.is_paid = 1 AND r.date >= CURRENT_DATE
                ORDER BY r.date
            """, [attraction.id])

            reservations = cursor.fetchall()
            # reservations_dict[attraction.id] = reservations
            # print(reservations_dict,"fsdghjkhgfbdv")
            # 预约数据分类
            for reservation in reservations:
                cursor.execute("""
                    SELECT username FROM users_user WHERE id = %s
                """, [reservation[1]])
                user_info = cursor.fetchone()
                reservation_data = {
                    'reservation_id': reservation[0],
                    'user_name': user_info[0],
                    'contact_name': reservation[2],
                    'contact_phone': reservation[3],
                    'note': reservation[4],
                    'created_at': reservation[5],
                    'reservation_name': reservation[7]
                }
                #print(type(reservation[6]),reservation[6],"sdgfhghkgfdsdbdfgfng")
                if reservation[6] == 'approve':
                    approved_reservations.append(reservation_data)
                elif reservation[6] == 'reject':
                    rejected_reservations.append(reservation_data)
                else:
                    upcoming_reservations.append(reservation_data)
    print(daily_reservations,"asdfghjgfddf")
    # daily_reservations = {
    #     "2024-11-16": 2,
    #     "2024-11-17": 5
    # }
    return render(request, 'manager_dashboard.html', {
        'approved_reservations': approved_reservations,
        'rejected_reservations': rejected_reservations,
        'upcoming_reservations': upcoming_reservations,
        'next_month_count': next_month_count,
        'daily_reservations': daily_reservations
    })


@login_required
@user_passes_test(manager_required)
def batch_update_reservations(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        reservation_ids = request.POST.getlist('reservation_ids')
        print(reservation_ids, action)

        # 检查用户是否选择了预约并根据action来更新状态
        if reservation_ids and action in ['approve', 'reject']:
            status = 'approve' if action == 'approve' else 'reject'

            # 构建 IN 子句的占位符，动态生成占位符数量
            placeholders = ', '.join(['%s'] * len(reservation_ids))  # 使用 %s 作为占位符
            params = [status] + reservation_ids  # 第一个参数是 status，后面是 reservation_ids

            # 执行 SQL 查询，更新状态
            with connection.cursor() as cursor:
                sql_query = f"""
                    UPDATE attractions_reservation
                    SET status = %s
                    WHERE id IN ({placeholders})
                """
                print(f"SQL query: {sql_query}, Parameters: {params}")  # 打印调试信息
                cursor.execute(sql_query, params)

    return redirect('manager_dashboard')


@login_required
@user_passes_test(manager_required)
def approve_reservation(request, reservation_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attractions_reservation
            SET status = 'approve'
            WHERE id = %s
        """, [reservation_id])
    return redirect('manager_dashboard')


@login_required
@user_passes_test(manager_required)
def reject_reservation(request, reservation_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attractions_reservation
            SET status = 'reject'
            WHERE id = %s
        """, [reservation_id])
    return redirect('manager_dashboard')


def manager_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # 如果是景区管理员，允许登录
            if user.role in ['attraction_manager']:
                login(request, user)
                return redirect('manager_dashboard')
            else:
                return redirect('login')  # 如果不是管理员，跳转到普通用户登录
    else:
        form = AuthenticationForm()

    return render(request, 'manager_login.html', {'form': form})


