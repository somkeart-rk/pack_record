import streamlit as st
import pandas as pd
import include.db as db
#from datetime import datetime, timedelta

def updateTimeList():
    st.session_state["ShiftType"] = st.session_state["pShiftType"][0:2]
    st.session_state["group_Type"] = st.session_state["pGroupType"]
    # db.loadTimeRange("PACK","AD")
    st.session_state['pTimeList']  = pd.DataFrame(db.loadTimeRange("PACK",st.session_state["ShiftType"]))
    #st.write(st.session_state['pTimeList'] )
    return st.session_state['pTimeList']
    
def packtrans():
    st.session_state['firstLoop'] = True
    if 'ShiftType' not in st.session_state:
        st.session_state['ShiftType'] = "AD"
        st.session_state['pTimeList'] = []
        st.session_state["group_Type"] = "PACK"
        
    st.markdown("<h2 style='text-align: center; color: blue;'>ข้อมูลการบรรจุ</h2>", unsafe_allow_html=True)
    with st.container():
        col1,col2,col3,col4 = st.columns(4)
        groupType = col1.selectbox("ประเภทงาน",["PACK","EMB"],key="pGroupType")
        workDay = col2.date_input("วันที่ทำงาน")
        # ไม่สามารถใช้งาน on_change ของ selectbox ได้ขณะอยู่ในภายใน Form ได้
        shiftType = col3.selectbox("กะ",["AD 08:00 - 17:00","AN 20:00 - 05:00","BD 08:00 - 17:00","BN 20:00 - 05:00","DD 08:00 - 17:00"],key="pShiftType",on_change=updateTimeList)
        if st.session_state['firstLoop']:
            updateTimeList()
            st.session_state['firstLoop'] = False

        cellGroup = col4.selectbox("Line/Cell",db.loadLineCell("PACK"))
        col1,col2,col3,col4 = st.columns([1.25,2,1,1])
        timeCode = col1.selectbox("เวลาทำงาน",options=st.session_state['pTimeList'] )
        styleCode = col2.selectbox("สไตล์งาน : จำนวนงานต่อชั่วโมง",db.loadStyleTarget(st.session_state["group_Type"],"EMPLOYEE"),index=0)
        actualPack = col3.number_input("ทำได้จริง",step=1)
        actualDefect = col4.number_input("งานเสีย",step=1)
        col1,col2 = st.columns([2,2])
        problemCause = col1.text_area("สาเหตุที่ไม่ได้เป้าหมาย",max_chars=1020)
        solutionCause = col2.text_area("แนวทางแก้ใข",max_chars=1020)

    submitted = st.button("บันทึกข้อมูล")
    if submitted:
        if actualPack != 0:
            loginName= st.session_state["userName"]
            targetStart = styleCode.find(" : ")+2
            targetEnd = styleCode.find(" Pairs")
            targetCurrent = styleCode[targetStart:targetEnd]
            #st.write(f" data : {groupType} : {workDay} : {shifType[0:2]} : {cellGroup[0]} : {cellGroup[-2:]} : {timeCode} : {styleCode[0:targetStart-2]} : {targetCurrent} : {actualPack} : {actualDefect} ")
            #st.write(f" data : {problemCause} : {solutionCause} : {loginName} ")

            sql = "INSERT INTO `tsc_main_db`.`trans_pack_finish`(`group_type`,`work_day`,`shift`,`line_pack`,`cell_pack`,`time_text`,`style_code`,`current_target`,`actual_target`,"
            sql += "`actual_defect`,`problem_cause`,`solution_cause`,`user_create`) "
            sql += f" VALUES('{groupType}','{workDay}','{shiftType[0:2]}','{cellGroup[0]}','{cellGroup[-2:]}','{timeCode}','{styleCode[0:targetStart-2]}',{targetCurrent},{actualPack}," 
            sql += f" {actualDefect},'{problemCause}','{solutionCause}','{loginName}' ); "
            #st.write(sql)
            db.run_saveData(sql)
            st.info("บันทึกข้อมูลเรียบร้อย")
        else:
            st.warning("ไม่มียอดการบรรจุ")

        
