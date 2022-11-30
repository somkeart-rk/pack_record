import streamlit as st
import pandas as pd
import include.db as db
from datetime import datetime, timedelta
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

def newStyle():

    with st.form("new_style_form"):
        col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])
        groupType = col1.selectbox("ประเภทงาน *",["PACK","EMB"])
        styleCode = col2.text_input("สไตล์งาน *")
        targetHour = col3.number_input("เป้าหมาย/ชั่วโมง",value=0,step=1)
        unitType = col4.selectbox("หน่วยนับ",["Pairs","Piece"])
        col5.markdown("<h1 style='text-align: center; color: blue;'></h1>", unsafe_allow_html=True)
        submitted = col5.form_submit_button("เพิ่มข้อมูล")
        if submitted:
            if targetHour > 0:
                loginName= st.session_state["userName"]
                sql = "INSERT INTO `tsc_main_db`.`style_target`(`style_type`,`style_code`,`machine_type`,`target_hour`,`unit`,"
                sql += "`active`,`active_date`,`user_create`) "
                sql += f" VALUES('{groupType}','{styleCode}','EMPLOYEE',{targetHour},'{unitType}','Y'," 
                sql += f" NOW(),'{loginName}' ); "
                #st.write(sql)
                db.run_saveData(sql)
                st.info("บันทึกข้อมูลเรียบร้อย")
            else:
                st.warning("ไม่มีข้อมูล")
        col1.write("ระบุข้อมูลในช่องที่มี *")
        findStyle = col1.form_submit_button("ตรวจสอบ")
        if findStyle:
            if styleCode:
                sql = "select `style_type`,`style_code`,`target_hour`,`unit`,`active_date`  from `tsc_main_db`.`style_target` "
                sql += f" where active='Y' and `style_type`='{groupType}' and `style_code` like '%{styleCode}%' " 
                df = db.run_query(sql)
                rows = pd.DataFrame(df,columns=["ประเภทงาน","สไตล์งาน","เป้าหมายต่อชั่วโมง","หน่วยนับ","เริ่มใช้งาน"])
                AgGrid(rows, fit_columns_on_grid_load=True)
            else:
                st.warning("ไม่มีข้อมูล")
            
