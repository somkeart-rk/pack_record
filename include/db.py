import streamlit as st
import pymysql as connection
import pandas as pd

def init_connection():
    return connection.connect(**st.secrets["mysql"])

#conn = init_connection()

#Select data from database
def run_query(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    finally:
        conn.close()

#Save data to database
def run_saveData(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            #st.info("Save data")
    finally:
        conn.close()

def check_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.check_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()

def update_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.update_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    finally:
        conn.close()

#load machine type data list for selectBox
def load_machineType():
    sql = "select distinct t0.machine_type from sms_db.tbl_running t0 "
    sql += " order by t0.running_id "
    rows = run_query(sql)
    return pd.DataFrame(rows)

#load service group data list for selectbox
def loadServiceGroup(service_No):
    sql = "select distinct t0.service_group from sms_db.tbl_service_group t0, sms_db.tbl_service_list t1 "
    sql += f" where t1.service_no='{service_No}' and t0.machine_type=t1.machine_type order by t0.service_group_id "
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["service_group"])

#load employee code data list to selectbox
def loadEmployeeCode(divisionCode):
    sql = 'select  distinct t0.emp_code2 '
    sql += ' from hr_system.employee t0 '
    sql += f' where t0.division_code="{divisionCode}" and t0.active="Y" '
    sql += ' order by t0.emp_code2 asc '
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["emp_code2"])

#load employee name data list to selectbox
def findEmployeeName(employeeCode):
    sql = 'select distinct concat(t0.emp_fname," ",t0.emp_lname) as emp_name '
    sql += ' from hr_system.employee t0 '
    sql += f' where t0.emp_code2="{employeeCode}" and t0.active="Y" '
    sql += ' order by t0.emp_work_startdate desc limit 1 '
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["emp_name"])

#load Line and Cell data list to selectbox
def loadLineCell(lineGroup):
    sql = 'select distinct concat(t0.line_code,"/",t0.machine_code) line_cell '
    sql += ' from tsc_main_db.machine_line t0 '
    sql += f' where t0.line_group="{lineGroup}"  '
    sql += ' order by t0.line_code ,t0.machine_code asc  '
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["line_cell"])

#load time range data list to selectbox
def loadTimeRange(divisionCode,shiftCode):
    #st.write(f"{divisionCode} : {shiftCode}")
    sql = 'select  distinct t0.time_text '
    sql += ' from tsc_main_db.time_range t0 '
    sql += f' where t0.time_template="{divisionCode}" and t0.shift="{shiftCode}"  '
    sql += ' order by t0.id asc '
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["time_text"])

#load style target data list to selectbox
def loadStyleTarget(divisionCode,machineCode):
    sql = 'select  distinct concat(t0.style_code," : ",t0.target_hour," Pairs") as style_Code '
    sql += ' from tsc_main_db.style_target t0 '
    sql += f' where t0.style_type="{divisionCode}" and t0.machine_type="{machineCode}" and t0.active="Y" '
    sql += ' order by t0.style_code asc '
    rows = run_query(sql)
    return pd.DataFrame(rows,columns=["style_Code"])
