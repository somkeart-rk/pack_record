from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np 
import pymysql as connection
import include.db as db
import include.export_tools as exp
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode


# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data(startDate,finishDate,groupType,shiftType,cellGroup):

    sql = "select t0.group_type,date_format(t0.work_day,'%Y-%m-%d') work_day,t0.shift,concat(t0.line_pack,'/',t0.cell_pack) line_pack,t0.time_text,t0.style_code,t0.current_target "
    sql += " ,t0.actual_target "
    sql += ",(select group_concat(t10.emp_code) from tsc_main_db.set_man_power t10 "
    sql += f" where t10.group_type='{groupType}' and t10.shift='{shiftType[0:2]}' and t10.line_code='{cellGroup[0]}' and t10.machine_code='{cellGroup[-2:]}' "
    sql += f" and date_format(t10.start_date,'%Y-%m-%d')='{startDate}') as emp_code "
    sql += " from tsc_main_db.trans_pack_finish t0 "
    sql += f" where  t0.group_type ='{groupType}' and t0.shift = '{shiftType[0:2]}' and t0.line_pack ='{cellGroup[0]}' "
    sql += f" and t0.cell_pack = '{cellGroup[-2:]}' "
    sql += f" and (date_format(t0.work_day,'%Y-%m-%d') = '{startDate}' ) "
    #sql += f" and (date_format(t1.finish_date,'%Y-%m-%d') between date'{startDate}' and '{finishDate}' ) "
    sql += " order by t0.id asc; "
    #st.write(sql)
    st.info("รายการประวัติการทำงาน")
    rows = db.run_query(sql)
    #return pd.DataFrame(rows)
    return pd.DataFrame(rows,columns=["ประเภทงาน","วันที่ทำงาน","กะทำงาน","สาย/Cell","เวลาทำงาน","สไตล์งาน","เป้าหมาย","ทำได้จริง","ผู้รับผิดชอบ"])
    
def showhistiryjob():
    with st.container():
        st.markdown("<h2 style='text-align: center; color: blue;'>ประวัติการบรรจุ</h2>", unsafe_allow_html=True)

        col1, col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])

        st_d = col1.date_input("วันที่เริ่ม")
        fn_d = col2.date_input("วันสุดท้าย")
        shiftType = col3.selectbox("กะ",["AD 08:00 - 17:00","AN 20:00 - 05:00","BD 08:00 - 17:00","BN 20:00 - 05:00","DD 08:00 - 17:00"])
        groupType = col4.selectbox("ประเภทงาน",["PACK","EMB"])
        cellGroup = col5.selectbox("Line/Cell",db.loadLineCell("PACK"))

        col6.markdown("<h1 style='text-align: center; color: blue;'></h1>", unsafe_allow_html=True)
        if col6.button("ค้นหา"):
            #st.write(st_d," ",fn_d)
            df = load_data(st_d,fn_d,groupType,shiftType,cellGroup)
            #st.dataframe(df, use_container_width=True)
            AgGrid(df, fit_columns_on_grid_load=True)
            st.download_button(label="download as Excel-file",
                data=exp.convert_to_excel(df),
                file_name="export_pack_history.xls",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="Pack Data",
            )

        else:
            st.write('Not Select')




    