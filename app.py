import streamlit as st
from streamlit_option_menu import option_menu
#from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import base64
import include.db as db
import services.newjob as nj
import services.showjob as sj
import services.packtrans as pt
import services.historyjob as hj
import config_menu as conf_menu

st.set_page_config(layout="wide")

if "login" not in st.session_state:
    st.session_state["login"] = False
    st.session_state.userName = ""
    st.session_state.fullName = ""

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

if not st.session_state["login"]:
    
    with st.form("login_form"):
        imgCol1,imgCol2,imgCol3 = st.columns([1.5,1,2])
        my_logo = add_logo(logo_path="./img/logo.jpg", width=206, height=122)
        imgCol2.image(my_logo,use_column_width=False)
        st.markdown("<h2 style='text-align: center; color: blue;'>ระบบบันทึกข้อมูลการบรรจุ</h2>", unsafe_allow_html=True)

        userName = st.text_input("รหัสพนักงาน").upper()
        passWord = st.text_input("รหัสผ่าน","",20,None,"password")
        submitted = st.form_submit_button("เข้าใช้งานระบบ")
        if submitted:
            if "login" in st.session_state:
                #แปลงค่ารหัสผ่านให้เป็น base64
                enPassword = passWord.encode('ascii')
                b64_bytes = base64.b64encode(enPassword)
                #แปลงจาก Byte to string
                #st.write(b64_bytes.decode("ascii"))
                #st.write(b64_bytes)
                #ตรวจสอบข้อมูลเจ้าหน้าที่
                sql = 'select  t0.emp_code,concat(t1.emp_fname," ",t1.emp_lname) user_name,t0.password_remark '
                sql += ' from tsc_datacenter.user_data t0,hr_system.employee t1 '
                sql += f' where t0.user_name="{userName}" and t0.password_remark="{b64_bytes.decode("ascii")}" '
                sql += ' and t0.active="Y" and t0.emp_code=t1.emp_code2 '
                #st.write(sql)
                rows = db.run_query(sql)
                if  rows:
                    st.session_state["login"] = True
                    st.session_state.userName = userName
                    for row in rows:
                        #st.write(f"{row[0]} has a :{row[1]}:")
                        st.session_state.fullName = row[1]
                    st.experimental_rerun()
                else:
                    st.info("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                    #enPassword = 'bWFoYWxv'  #passWord.encode('ascii')
                    #b64_bytes =    base64.b64decode('bWFoYWxv')
                    #st.write(b64_bytes)
                    #st.write(b64_bytes.decode("ascii"))

def side_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title = None,
            options = ["ข้อมูลการบรรจุ","พนักงานประจำไลน์","ประวัติการบรรจุ", "ตั่งค่า", "Logout"],
            icons = ["list-task","file","book","gear","key"],
            menu_icon = "cast",
            default_index = 0,
            #orientation = "horizontal",
            #styles={
            #        "container": {"padding": "0!important", "background-color": "#0a0afa"},
            #        "icon": {"color": "orange", "font-size": "16px"}, 
            #        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            #        "nav-link-selected": {"background-color": "green"},
            #    }
        )
        if "login" in st.session_state:
            st.write('รหัสพนักงาน : ',st.session_state["userName"] )
            st.write('ชื่อพนักงาน  : ',st.session_state["fullName"] )

    if selected == "พนักงานประจำไลน์":
        nj.newjob()
    if selected == "ข้อมูลการบรรจุ":
        pt.packtrans()
    if selected == "ประวัติการบรรจุ":
        hj.showhistiryjob()
    if selected == "ตั่งค่า":
        conf_menu.top_menu()
    if selected == "Logout":
        with st.form("logout_form"):
            st.header("Logout")
            st.write("Confirme Logout")

            submitted = st.form_submit_button("Logout")
            if submitted:
                if "login" in st.session_state:
                    st.session_state["login"] = False
                    st.experimental_rerun()


if st.session_state["login"]:
    side_menu()

st.write(st.session_state["login"])

