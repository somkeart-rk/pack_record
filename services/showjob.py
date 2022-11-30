import time
import numpy as np
import pandas as pd
import streamlit as st
import services.newjob as nj
import include.db as db
import include.export_tools as exp


@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def color_priority(val):
    color = 'red' if val == '3-HIGH' else 'black'
    return 'color:{}'.format(color)   

def showjob():
    st.header("งานที่กำลังทำ")
    loginName= st.session_state["userName"]
    # # Show user table 
    st.markdown(
        """ <style> 
            .font {font-size:16px;} 
            .standart-text {font-size:14px; }
            </style> 
        """, unsafe_allow_html=True)

    colms = st.columns((1, 1, 1, 2, 1),gap="small")
    fields = ["№", 'Service No', 'M/C No', 'Detail', 'Status']
    for col, field_name in zip(colms, fields):    # header
        col.write(field_name)

    sql = "select service_list_id,service_no,machine_no,trim(service_detail) service_detail,status "
    sql += f" from sms_db.tbl_service_list where status='OPEN' and support_id like '{loginName}' "
    sql += " order by left(priority_type,1) desc,create_date asc ;"
    rows = db.run_query(sql)
    service_table=pd.DataFrame(rows,columns=["№","service_no","machine_no","service_detail","status"])

    for x, service_no in enumerate(service_table['service_no']):
        col1, col2, col3, col4, col5 = st.columns((1, 1, 1, 2,1),gap="small")
        col1.write(x)  
        col2.write(service_table['service_no'][x])  
        col3.write(service_table['machine_no'][x])  
        col4.write(service_table['service_detail'][x])  
        disable_status = service_table['status'][x]  
        button_type = "Close" if disable_status else "OPEN"
        button_phold = col5.empty()  
        do_action = button_phold.button(button_type, key=x)
        if do_action:
            button_phold.empty()  
            serviceNo = service_table['service_no'][x]
            nj.Closejob(service_no)

    st.download_button(label="download as Excel-file",
        data=exp.convert_to_excel(service_table),
        file_name="export_Ready_Job.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="excel_download",
    )
    
