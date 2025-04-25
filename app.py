import streamlit as st
import pandas as pd

# Load attendance data
@st.cache_data
def load_data():
    df = pd.read_excel("Book2.xlsx")
    return df

df = load_data()

st.title("نظام معلومات الموظف وسجل الحضور")

# البحث برقم الهوية (ID#)
search_input = st.text_input("أدخل رقم الهوية (ID#):")

result = df[df['ID#'].astype(str).str.contains(search_input)]

if not result.empty:
    st.subheader("معلومات الموظف العامة:")
    st.dataframe(result[["EMP#", "ID#", "NAME (ENG)", "NAME (AR)", "NATIONALITY", "POSITION", "COMPANY"]].drop_duplicates())

    if st.button("عرض سجل الحضور الأسبوعي"):
        st.subheader("سجل الحضور الأسبوعي:")
        attendance_days = result[["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]]
        st.dataframe(attendance_days)

        # حساب عدد أيام الغياب
        absence_count = (attendance_days == 0).sum(axis=1).values[0]
        st.info(f"عدد أيام الغياب خلال الأسبوع: {absence_count} يوم")
else:
    if search_input:
        st.warning("لم يتم العثور على الموظف برقم الهوية.")

# زر عرض الموظفين الذين يداومون جمعة أو سبت أو اثنين
if st.button("عرض الموظفين الذين يداومون الجمعة أو السبت أو الاثنين"):
    friday = df[(df['FRI'] == 1) & (df['SAT'] != 1)]
    saturday = df[(df['SAT'] == 1) & (df['FRI'] != 1)]
    monday_plus = df[(df['MON'] == 1) & ((df['FRI'] == 1) | (df['SAT'] == 1))]

    final = pd.concat([
        friday.assign(ملاحظة="مداوم يوم الجمعة فقط"),
        saturday.assign(ملاحظة="مداوم يوم السبت فقط"),
        monday_plus.assign(ملاحظة="مداوم الاثنين + الجمعة/السبت")
    ])

    st.subheader("نتائج الموظفين الخاصة:")
    st.dataframe(final[["EMP#", "ID#", "NAME (ENG)", "NAME (AR)", "FRI", "SAT", "MON", "ملاحظة"]])
