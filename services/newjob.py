import streamlit as st
import pandas as pd
import include.db as db
#import datetime
from datetime import datetime, timedelta

def newjob():
    data = pd.DataFrame()

    if 'df' not in st.session_state:
        st.session_state.df = data
        st.session_state.firstLoop = True
        st.session_state.checkDup = False
        
    with st.form("new_form"):
        st.markdown("<h2 style='text-align: center; color: blue;'>กำหนดพนักงานประจำไลน์</h2>", unsafe_allow_html=True)

        col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])
        groupType = col1.selectbox("ประเภทงาน",["PACK","EMB"])
        workDay = col2.date_input("วันที่ทำงาน")
        shifType = col3.selectbox("กะ",["AD 08:00 - 17:00","AN 20:00 - 05:00","BD 08:00 - 17:00","BN 20:00 - 05:00","DD 08:00 - 17:00"])
        cellGroup = col4.selectbox("Line/Cell",db.loadLineCell("PACK"))
        empCode = col5.selectbox("รหัสพนักงาน",db.loadEmployeeCode("SCK"))
        col6.markdown("<h1 style='text-align: center; color: blue;'></h1>", unsafe_allow_html=True)
        addEmployee = col6.form_submit_button("เพิ่ม")
        if addEmployee:

            #Add data in first loop
            if st.session_state.firstLoop == True:
                #df = df.append({'data': st.session_state[item]}, ignore_index=True)
                #st.write(empCode)
                empName = db.findEmployeeName(employeeCode=empCode)
                emp_Name = empName["emp_name"].unique()
                #st.write(empName)
                df_newRow = pd.DataFrame({'รหัสพนักงาน': [empCode],'ชื่อ - นามสกุล': [emp_Name]})
                st.session_state.df = pd.concat([st.session_state.df,df_newRow],ignore_index=True)
                st.session_state.firstLoop = False
            else:
                #Check duplicate empCode
                for item in st.session_state.df:
                    values = st.session_state.df[item].tolist()
                    total = 0
                    for value in values:
                        #st.write(values[total])
                        if empCode == values[total]:
                            st.session_state.checkDup = True
                            st.warning("มีข้อมูลแล้ว")
                        total = total + 1

                #st.write(st.session_state.df)
                if st.session_state.checkDup == False:
                    empName = db.findEmployeeName(employeeCode=empCode)
                    emp_Name = empName["emp_name"].unique()
                    #st.write(f"2 : {empName}")
                    df_newRow = pd.DataFrame({'รหัสพนักงาน': [empCode],'ชื่อ - นามสกุล': [emp_Name]})
                    st.session_state.df = pd.concat([st.session_state.df,df_newRow],ignore_index=True)

            st.write("รายชื่อพนักงานประจำโต๊ะ")
            st.dataframe(st.session_state.df,use_container_width=True)
            st.session_state.checkDup = False

        submitted = st.form_submit_button("บันทึกข้อมูล")
    if submitted:
        if not pd.DataFrame(st.session_state.df).empty:
            loginName= st.session_state["userName"]
            #Check running data from server
            for x,emp_Code in enumerate(st.session_state.df['รหัสพนักงาน']):
                #empCode = st.session_state.df['รหัสพนักงาน'][x]
                #st.write(emp_Code)
                if shifType[0] == 'B':
                    workDay_str = f"{workDay.year}-{workDay.month}-{workDay.day+1}"
                    workDayEnd = datetime.strptime(workDay_str, '%Y-%m-%d')
                else:
                    workDayEnd = workDay
                #st.write(f" data : {empCode} : {cellGroup[0]} : {cellGroup[-2:]} : {shifType[0:2]} : {workDay} : {shifType[3:8]} : {workDayEnd} : {shifType[-5:]} : {loginName} ")
                sql = "INSERT INTO `tsc_main_db`.`set_man_power`(`group_type`,`set_type`,`emp_code`,`line_code`,`machine_code`,"
                sql += "`shift`,`start_date`,`start_time`,`end_date`,`end_time`,`approve_status`,`user_create`) "
                sql += f" VALUES('{groupType}','N','{emp_Code}','{cellGroup[0]}','{cellGroup[-2:]}','{shifType[0:2]}','{workDay}'," 
                sql += f" '{shifType[3:8]}','{workDayEnd}','{shifType[-5:]}','N','{loginName}' ); "
                #st.write(sql)
                db.run_saveData(sql)
            st.info("บันทึกข้อมูลเรียบร้อย")
        else:
            st.warning("ไม่มีข้อมูล")
        del st.session_state.df

            
def Closejob(service_No):
    CloseJob_form = st.form(key="Close Job")
    if 'pChange' not in st.session_state:
        st.session_state['pChange'] = ''
        st.session_state['sDetail'] = ''

    CloseJob_form.subheader("บันทึกรายละเอียดการซ่อม")
#    serviceGroup = CloseJob_form.selectbox(f"ประเภทการซ่อม",["เปลี่ยนเข็ม","ปรับตั้งเครื่อง"]) 
    serviceGroup = CloseJob_form.selectbox(f"ประเภทการซ่อม",db.loadServiceGroup(service_No)) 
    CloseJob_form.text_input("อุปกรณ์ที่เปลี่ยน",key="pChange",max_chars=199 )
    CloseJob_form.text_area(f"รายละเอียดการซ่อม",key="sDetail",max_chars=1000)
    CloseJob_form.form_submit_button("ปิดงานซ่อม",on_click=saveData,args=[service_No,serviceGroup,])


def saveData(service_No,serviceGroup,):
    partChange = st.session_state.pChange
    serviceDetail = st.session_state.sDetail
    sqlUpdate = f"UPDATE `sms_db`.`tbl_service_list` SET `status`= 'CLOSE' WHERE `service_no`='{service_No}'; "
    #st.write(sqlUpdate)
    db.run_saveData(sqlUpdate)

    sqlAddDetail = "INSERT INTO `sms_db`.`tbl_service_detail`(`service_no`,`service_group`,`part_detail`,`service_detail`) "
    sqlAddDetail += f" VALUES('{service_No}','{serviceGroup}','{partChange}','{serviceDetail}'); "
    #st.write(sqlAddDetail)
    db.run_saveData(sqlAddDetail)
    st.info(f"งานหมายเลข : {service_No} ปิดเรียบร้อย")
    #time.sleep(0.5)
 