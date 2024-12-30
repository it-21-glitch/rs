import os
import uuid
import json
import time
import sqlite3
import pandas as pd
from datetime import datetime
from flask import request, render_template, make_response

from config import get_db, generation_xlsx


# 首页
def factory_index():
    """
        工厂使用的首页
    :return: index首页
    """
    title = 'RS工厂首页'
    per_page = 12  # 每页显示12条记录
    page = int(request.args.get('page', 1))
    db_conn = get_db()
    cursor = db_conn.cursor()
    po = request.args.get('po')
    item = request.args.get('item')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conditions = ''
    conditions_list = []
    if po:
        conditions_list.append(f"po='{po}'")
    if item:
        conditions_list.append(f"item='{item}'")
    if start_date:
        conditions_list.append(f"strftime('%Y-%m-%d', entry_time) >= datetime('{start_date}')")
    if end_date:
        conditions_list.append(f"strftime('%Y-%m-%d', entry_time)  <= datetime('{end_date}')")
    conditions_list.append("examine_status == 1")
    if conditions_list:
        conditions = ' AND '.join(conditions_list)
    if not conditions:
        get_total_sql = """
           SELECT COUNT(*) FROM  main.record_sheet WHERE examine_status == 1
       """
    else:
        get_total_sql = f"""
               SELECT COUNT(*) FROM  main.record_sheet WHERE {conditions}
           """
    cursor.execute(get_total_sql)
    data_total = cursor.fetchone()[0]  # 数据总数
    page_total, page_remainder = divmod(data_total, 12)  # 页码数
    if page_total != 0:
        page_total += 1
    if not conditions:
        get_sql = f"""
            SELECT 
                main.record_sheet.id,
                main.record_sheet.entry_time,
                main.record_sheet.po,
                main.record_sheet.item,
                main.record_sheet.people_number,
                main.record_sheet.output_number,
                main.record_sheet.examine_status,
                main.record_sheet.examine_time,
                main.record_sheet.material_name,
                main.record_sheet.equipment_name,
                main.record_sheet.process_name,
                main.record_sheet.specification_name,
                main.record_sheet.attendance_picture
            FROM 
                main.record_sheet
            WHERE examine_status == 1
             ORDER BY id DESC 
            LIMIT {per_page} OFFSET {(page - 1) * 12};
        """
    else:
        get_sql = f"""
                SELECT 
                    main.record_sheet.id,
                    main.record_sheet.entry_time,
                    main.record_sheet.po,
                    main.record_sheet.item,
                    main.record_sheet.people_number,
                    main.record_sheet.output_number,
                    main.record_sheet.examine_status,
                    main.record_sheet.examine_time,
                    main.record_sheet.material_name,
                    main.record_sheet.equipment_name,
                    main.record_sheet.process_name,
                    main.record_sheet.specification_name,
                    main.record_sheet.attendance_picture
                FROM 
                    main.record_sheet
                WHERE {conditions}
                 ORDER BY id DESC 
                LIMIT {per_page} OFFSET {(page - 1) * 12};
                """
    cursor.execute(get_sql)
    column_names = [description[0] for description in cursor.description]
    data_list_all = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    pagination_links = []
    # 然页面永远展示5条页码
    page_start_number = page
    page_end_number = 5 + (page - 1)  # 计算展示最后以为展示的页码
    if page_end_number > page_total:  # 计算起始的页码
        page_start_number = page_total - 4
    if page_total <= 5:  # 如果总页码小于等于5，那么起始页码不进行计算
        page_start_number = 1
    for i in range(page_start_number, min(page_total, page_end_number) + 1):
        if i == page:
            pagination_links.append((i, 'active'))  # 当前页不加链接
        else:
            pagination_links.append((i, f'?page={i}'))

    return render_template('factory_index.html', title=title, data_list_all=data_list_all, data_total=data_total,
                           page_total=page_total, pagination_links=pagination_links, page=page)


# 工厂添加记录页面
def factory_add_records():
    """
        工厂添加
    :return:
    """
    get_material_sql = """
        SELECT id,material_name FROM main.material
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(get_material_sql)
    column_names = [description[0] for description in cursor.description]
    data_list_all = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    db_conn.close()
    return render_template('factory_add_records.html', data_list_all=data_list_all)


# 获取工序,设备
def factory_get_equipment_and_process():
    """
        根据材质获取工序,根据工序获取设备,根据工序获取班次
    :return:
    """
    pk = request.args.get("pk")
    status = request.args.get("status")
    if not pk and not status:
        return {"code": 200, "data_list_all": []}
    db_conn = get_db()
    cursor = db_conn.cursor()
    if status == "process":
        get_sql = f"""
            SELECT id,process_name FROM main.process WHERE material_id='{pk}'
        """
    else:
        get_sql = f"""
            SELECT id,equipment_name FROM main.equipment WHERE process_id='{pk}'
        """

    cursor.execute(get_sql)
    column_names = [description[0] for description in cursor.description]
    data_list_all = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    db_conn.close()
    return {"code": 200, "data_list_all": data_list_all}


# 获取工序与设备的人员基本信息
def factory_get_information_description():
    """
        根据材质获取工序,根据工序获取设备,根据工序获取班次
    :return:
    """
    specs = request.args.get("specsSelect")  # 规则
    process = request.args.get("processSelect")
    equipment = request.args.get("equipmentSelect")
    get_sql = f"""
        SELECT  * FROM main.equipment WHERE process_id='{process}' AND id='{equipment}'
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute(get_sql)
    data = cursor.fetchone()
    if not data:
        return {"code": 200, "message": '', "day_classes_frequency": 0,
                'classes_man_hour': 0}
    column_names = [description[0] for description in cursor.description]
    data_dict = dict(zip(column_names, data))
    equipment_name = data_dict.get("equipment_name")
    equipment_number = data_dict.get("equipment_number")
    max_people_number = data_dict.get("max_people_number")
    min_people_number = data_dict.get("min_people_number")
    day_classes_frequency = data_dict.get("day_classes_frequency")
    classes_man_hour = data_dict.get("classes_man_hour")
    specs_number = data_dict.get(specs)
    person_number = round(specs_number / min_people_number)  # 班次个人产能
    message = f'使用设备：{equipment_name}，设备数量：{equipment_number}，工序最大人数：{max_people_number}，工序最小人数：{min_people_number}，班次：{day_classes_frequency}班，每班工时：{classes_man_hour}小时，班次产能：{specs_number}，班次个人产能：{person_number}。'

    # 获取工序名称
    get_process_sql = f"""
        SELECT process_name FROM main.process WHERE id = '{data_dict.get("process_id")}'
    """
    cursor.execute(get_process_sql)
    process_name = cursor.fetchone()[0]  # 工序的名称
    user_list = []  # 当前工序的员工列表
    file_path_json = os.path.join("static", 'roster.json')
    with open(file_path_json, mode='r', encoding='utf-8') as f:
        json_read_list = json.loads(f.read())
    for i in json_read_list:
        working_procedure = i.get("working_procedure")
        if process_name == working_procedure:
            user_list.append(i)
    cursor.close()
    db_conn.close()

    return {"code": 200, "message": message, "day_classes_frequency": day_classes_frequency,
            'classes_man_hour': classes_man_hour, "max_people_number": max_people_number,
            'min_people_number': min_people_number, "user_list": user_list}


# 附件获取
def factory_get_attendance_and_production_records():
    pk = request.form.get("pk")
    file_path = generation_xlsx(pk, get_db)
    if not file_path:
        return {"code": 500}
    return {"code": 200, 'file_path': file_path}


# 下载单独的记录的考勤与生产记录信息
def factory_download_attendance_and_production_records():
    examine_time = datetime.now().strftime('%Y-%m-%d')
    file_path = request.args.get("file_path")
    file_name = f'{examine_time}.zip'
    with open(file_path, mode='rb') as file:
        response = make_response(file.read())
        response.headers['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{file_name}'
        response.mimetype = 'text/html'  # 设置正确的 MIME 类型
        return response


# 文件删除信号，删除生成的考勤与生产记录信息
def factory_delete_attendance_and_production_records():
    file_path = request.args.get("file_path")
    status = False
    try:  # 尝试以读写模式打开文件
        with open(file_path, 'r+'):
            pass
    except IOError:
        status = True
    while status:
        print("文件正在使用中，请稍等片刻...")
        time.sleep(5)
    os.remove(file_path)
    return {"code": 200}


# 记录添加
def factory_add_record():
    uuid4_file_name = uuid.uuid4()
    file = request.files.get("file")
    data = request.form
    po = data.get("po")  # po
    item = data.get("item")  # item
    add_date = data.get("add_date")  # 时间
    if not add_date:
        add_date = datetime.now().strftime('%Y-%m-%d')
    specs = data.get("specsSelect")  # 规格
    user_list = json.loads(data.get("userList"))  # 用户列表
    process_id = data.get("processSelect")  # 工序
    material_id = data.get("materialSelect")  # 材质
    equipment_id = data.get("equipmentSelect")  # 设备
    classes_production_quantity_number = data.get("classes_production_quantity_number")  # 产能数量
    db_conn = get_db()
    cursor = db_conn.cursor()
    # 1.根据工序于设备,查询规则记录
    get_sql = f"""
        SELECT * FROM equipment WHERE process_id='{process_id}' AND id = '{equipment_id}'
    """
    cursor.execute(get_sql)
    column_names = [description[0] for description in cursor.description]
    data_dict = dict(zip(column_names, cursor.fetchone()))

    classes_capacity = data_dict.get(specs)  # 规格数量-班次的产能
    min_people_number = data_dict.get('min_people_number')  # 每天员工最多工作多少个小时
    person_number = round(classes_capacity / min_people_number)  # 每个班次每个人的个人产能

    # 2.员工数据
    user_data_list = []
    for index, i in enumerate(user_list):
        start_time = str(i.get("start_date")).replace("T", ' ')  # 开始时间
        end_time = str(i.get("end_date")).replace("T", ' ')  # 结束时间
        p_list = i.get("p_lit")
        for j in p_list:
            user_id = j.get("employee")
            pay = j.get("pay")
            if not user_id or not pay:
                return {'code': 500, "error": f"员工薪酬或用户未选中！"}
            user_data_list.append({
                "start_time": start_time,
                "end_time": end_time,
                "user_id": user_id,
                "pay": pay,
            })
    specification_dict = {
        "classes_capacity_big": "大号",
        "classes_capacity_middle": "中号",
        "classes_capacity_small": "小号",
    }
    # 产量判断
    if int(classes_production_quantity_number) == 0:
        return {'code': 500, "error": f"产能输入错误，产量不能为0！"}
    if person_number * len(user_data_list) != int(classes_production_quantity_number):
        return {'code': 500, "error": f"产能输入错误，产能应为:{person_number * len(user_data_list)}！"}
    if len(user_data_list) == 0 and int(classes_production_quantity_number) == 0:
        return {'code': 500, "error": f"产能输入错误,班次人员未选择！"}
    # 获取设备
    equipment_name = data_dict.get("equipment_name")
    # 获取材质名称
    get_material_name_sql = f"""
        SELECT material_name FROM main.material WHERE id = '{material_id}'
    """
    cursor.execute(get_material_name_sql)
    column_names = [description[0] for description in cursor.description]
    material_data_dict = dict(zip(column_names, cursor.fetchone()))
    material_name = material_data_dict.get("material_name")
    # 获取工序
    get_process_name_sql = f"""
         SELECT process_name FROM main.process WHERE id = '{process_id}'
     """
    cursor.execute(get_process_name_sql)
    column_names = [description[0] for description in cursor.description]
    process_data_dict = dict(zip(column_names, cursor.fetchone()))
    process_name = process_data_dict.get("process_name")
    if file:
        file_suffix = file.filename.split('.')[1]
        file_path = os.path.join('static', 'attendance_picture', f'{uuid4_file_name}.{file_suffix}')
        file_save_path = os.path.join(os.path.dirname(__file__), file_path)
        file.save(file_save_path)
    else:
        file_path = ''
    # 添加记录
    insert_sql = f"""
        INSERT INTO main.record_sheet
            (entry_time,po,item,specification_name,material_name,process_name,equipment_name,people_number,output_number,attendance_picture)
        VALUES
            (
            '{add_date}',
            '{po}',
            '{item}',
            '{specification_dict[specs]}',
            '{material_name}',
            '{process_name}',
            '{equipment_name}',
            '{len(user_data_list)}',
            '{classes_production_quantity_number}',
            '\\{file_path}')
    """
    try:
        cursor.execute(insert_sql)
        db_conn.commit()
    except sqlite3.Error as e:
        db_conn.rollback()
        return {'code': 500}
    insert_id = cursor.lastrowid
    # 添加考勤记录
    user_attendance_all_sql = ''
    for i in user_data_list:
        user_attendance_sql = f"""
            INSERT INTO
                main.factory_attendance_user(user_id,record_sheet_id,start_time,end_time,user_pay)
            VALUES ('{i.get('user_id')}','{insert_id}','{i.get('start_time')}','{i.get('end_time')}','{i.get('pay')}');
           """
        user_attendance_all_sql += user_attendance_sql
    try:
        cursor.executescript(user_attendance_all_sql)  # 使用executescript()执行多条SQL语句
        db_conn.commit()
    except sqlite3.Error as e:
        # 如果发生错误，回滚事务
        db_conn.rollback()
        return {'code': 500}
    return {'code': 200}


# 花名册模板下载
def factory_download_template_file_roster():
    file_path = os.path.join("static", 'template_xlsx', 'rosterTemplate.xlsx')
    file_name = 'roster_template.xlsx'
    with open(file_path, mode='rb') as file:
        response = make_response(file.read())
        response.headers['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{file_name}'
        response.mimetype = 'text/html'  # 设置正确的 MIME 类型
        return response


# 根据上传花名册进行员工添加
def factory_add_user():
    file = request.files.get("file")
    if not file:
        return {"code": 500}
    file_path = os.path.join("static", 'roster_template.xlsx')
    file_path_json = os.path.join("static", 'roster.json')
    file.save(file_path)
    df = pd.read_excel(file_path, sheet_name=0)
    # 判断表格头部格式
    if "工序" not in df.columns or "姓名" not in df.columns or "出生日期" not in df.columns:
        return {"code": 500}
    # 清空用户记录
    db_conn = get_db()
    cursor = db_conn.cursor()
    del_sql = """
        DELETE FROM main.factory_user;
    """
    try:
        cursor.executescript(del_sql)  # 使用executescript()执行多条SQL语句
        db_conn.commit()
    except sqlite3.Error as e:
        # 如果发生错误，回滚事务
        db_conn.rollback()
        return {"code": 500}
    user_list = []
    for index, row in df.iterrows():
        user_name = row.get("姓名")
        user_age = row.get("出生日期")
        working_procedure = row.get("工序")
        insert_sql = f"""
            INSERT INTO factory_user(user_name,user_age) VALUES ('{user_name}','{user_age}')
        """

        try:
            cursor.execute(insert_sql)
            db_conn.commit()
        except sqlite3.Error as e:
            db_conn.rollback()
            return {'code': 500}
        user_id = cursor.lastrowid
        user_list.append({
            "user_id": user_id,
            "user_name": user_name,
            "working_procedure": working_procedure
        })
    with open(file_path_json, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(user_list))
    os.remove(file_path)
    return {"code": 200}
