import streamlit as st
from streamlit_option_menu import option_menu
#from PIL import Image
#import base64
import include.db as db
import config.style_target as styleTarget

def top_menu():
    selected = option_menu(
        menu_title = None,
        options = ["ข้อมูลพนักงาน","ข้อมูลสไตล์งาน","ข้อมูลสายการทำงาน", "ข้อมูลเวลาทำงาน", "สูตรที่ใช้ในการทำงาน"],
        icons = ["list-task","file","book","gear","key"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal",
    )

    if selected == "ข้อมูลพนักงาน":
        st.info("Add Employee")
        #pt.packtrans()
    if selected == "ข้อมูลสไตล์งาน":
        #st.info("Set Style")
        styleTarget.newStyle()
    if selected == "ข้อมูลสายการทำงาน":
        st.info("ข้อมูลสายการทำงาน")
    if selected == "ข้อมูลเวลาทำงาน":
        st.info("ข้อมูลเวลาทำงาน")

