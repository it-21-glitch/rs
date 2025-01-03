import os
import sqlite3
import pandas as pd
from datetime import datetime
from flask import request, redirect, url_for, render_template, session, make_response

from config import VerifyForm, get_db, regular_function, rule_data_base


# RS登录
def rs_login():
    title = '登录'
    form = VerifyForm()
    user_name = session.get('username')
    if user_name:
        return redirect(url_for('rs.rs_index'))
    if form.validate_on_submit():  # csrf 验证
        db_conn = get_db()
        cursor = db_conn.cursor()
        user_name = request.form.get('name')
        user_pwd = request.form.get("pwd")
        sql = f"""
            SELECT * FROM main.user WHERE name='{user_name}' AND passwd='{user_pwd}'
        """
        try:
            cursor.execute(sql)
        except sqlite3.Error as e:
            return render_template('rs_login.html', form=form, title=title, error="没有这个样的用户或登录信息错误！")
        cursor.fetchone()
        session["username"] = user_name
        cursor.close()
        db_conn.close()
        return redirect(url_for('rs.rs_index'))

    return render_template('rs_login.html', form=form, title=title, error="")


# RS退出
def rs_logout():
    try:
        session.pop('username')
    except Exception as e:
        return {'code': 500}
    return {'code': 200}


# RS首页
def rs_index():
    per_page = 12  # 每页显示12条记录
    page = int(request.args.get('page', 1))
    form = VerifyForm()
    user_name = session.get('username')
    if not user_name:  # 没有cookie就退出登录页面
        return redirect(url_for('rs.rs_login'))
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
    if conditions_list:
        conditions = ' AND '.join(conditions_list)
    if not conditions:
        get_total_sql = """
        SELECT COUNT(*) FROM  main.record_sheet
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
    return render_template('rs_index.html', form=form, data_list_all=data_list_all, data_total=data_total,
                           page_total=page_total, pagination_links=pagination_links, page=page)


# RS规则规则
def rs_upload_attendance():
    file_name = 'rule.xlsx'
    user_name = session.get('username')
    if not user_name:  # 没有cookie就退出登录页面
        return redirect(url_for('login'))
    file = request.files.get("file")
    if not file:
        return {'code': 500}
    file.save(f"static/rule/{file_name}")
    rule_data_list = regular_function()
    df = pd.read_excel(f'static/rule/{file_name}', engine='openpyxl')
    df = df.fillna('')
    # 转换为HTML
    # html_table = tabulate(df, headers='keys', tablefmt='html')
    html_table = df.to_html(index=False, escape=False)
    # 将HTML保存到文件
    with open('static/rule/rule.html', 'w', encoding='utf-8') as f:
        f.write(html_table)

    if rule_data_list:
        db_conn = get_db()
        cursor = db_conn.cursor()
        status = rule_data_base(rule_data_list, cursor, db_conn)
        if not status:
            return {'code': 500}
    return {'code': 200}


# RS查看员工考勤
def rs_sign_in_record():
    pk = request.args.get('pk')
    if not pk:
        error = '数据错误，无法查询相关考勤记录！'
        data_list_all = []
    else:
        error = ''
        db_conn = get_db()
        cursor = db_conn.cursor()
        get_sql = f"""
            SELECT
                main.factory_user.user_name,
                main.factory_attendance_user.end_time,
                main.factory_attendance_user.start_time
            FROM
                main.factory_attendance_user
            INNER JOIN
                main.factory_user
            ON
                main.factory_user.id = main.factory_attendance_user.user_id
            WHERE
                main.factory_attendance_user.record_sheet_id = {pk}
        """
        cursor.execute(get_sql)
        column_names = [description[0] for description in cursor.description]
        data_list_all = [dict(zip(column_names, row)) for row in cursor.fetchall()]

    return render_template('rs_attendance.html', error=error, data_list_all=data_list_all)


# RS审核按钮
def rs_to_examine():
    pk = request.form.get('pk')
    if not pk:
        return {'code': 500}
    examine_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_examine_sql = f"""
        UPDATE main.record_sheet SET examine_time='{examine_time}',examine_status=1 WHERE id = '{pk}'
    """
    db_conn = get_db()
    cursor = db_conn.cursor()
    try:
        cursor.execute(update_examine_sql)
        db_conn.commit()
    except sqlite3.Error as e:
        db_conn.rollback()
        return {'code': 500}
    return {'code': 200}


# RS批量审核
def rs_to_examine_all():
    db_conn = get_db()
    cursor = db_conn.cursor()
    examine_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_examine_sql = f"""
        UPDATE main.record_sheet SET examine_time='{examine_time}',examine_status=1 WHERE examine_status = 0
    """
    try:
        cursor.execute(update_examine_sql)
        db_conn.commit()
    except sqlite3.Error as e:
        db_conn.rollback()
        return {'code': 500}
    return {'code': 200}


def rs_download_xlsx():
    file_path = os.path.join("static", 'template_xlsx', 'ruleTemplate.xlsx')
    file_name = 'rule_template.xlsx'
    with open(file_path, mode='rb') as file:
        response = make_response(file.read())
        response.headers['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{file_name}'
        response.mimetype = 'text/html'  # 设置正确的 MIME 类型
        return response
