import streamlit as st
import pandas as pd

# Load attendance data
@st.cache_data
def load_data():
    df = pd.read_excel("Book2.xlsx")
    return df

df = load_data()

st.set_page_config(layout="centered", page_title="نظام الموظف", page_icon="🗂️")
st.title("📋 نظام معلومات الموظف وسجل الحضور")

# البحث برقم الهوية
search_input = st.text_input("🔍 أدخل رقم الهوية الوطنية:")

result = df[df['ID#'].astype(str).str.contains(search_input)]

if not result.empty:
    st.subheader("👤 المعلومات العامة للموظف:")
    general_fields = [
        "EMP#", "NAME (ENG)", "NAME (AR)", "GENDER", "NATIONALITY",
        "ID#", "COMPANY", "POSITION", "POSITION_AR", "MRN", "LOCATION"
    ]
    available_fields = [col for col in general_fields if col in result.columns]
    data = result[available_fields].drop_duplicates().iloc[0]
    styled_data = pd.DataFrame(data).reset_index()
    styled_data.columns = ["العنصر", "القيمة"]
    st.dataframe(styled_data.style.set_properties(**{
        'background-color': '#f7f7f7',
        'border-color': 'black',
        'color': 'black',
        'font-size': '14px'
    }), use_container_width=True)

    if st.button("📅 عرض سجل الحضور الأسبوعي"):
        st.subheader("🕒 الحضور الأسبوعي:")
        days_cols = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        attendance = result[days_cols].T.reset_index()
        attendance.columns = ["اليوم", "الحالة"]
        st.dataframe(attendance.style.set_properties(**{
            'background-color': '#eaf2ff',
            'color': 'black',
            'font-size': '14px'
        }), use_container_width=True)

        # حساب الغياب من الأحد إلى الخميس
        work_days = ["SUN", "MON", "TUE", "WED", "THU"]
        absence_count = (result[work_days] == 0).sum(axis=1).values[0]
        st.success(f"عدد أيام الغياب (من الأحد إلى الخميس): {absence_count} يوم")
else:
    if search_input:
        st.warning("⚠️ لم يتم العثور على الموظف برقم الهوية.")

# الموظفون الذين يداومون جمعة أو سبت أو كلاهما فقط
if st.button("📊 عرض الموظفين الذين يداومون الجمعة أو السبت أو كلاهما"):
    friday = df[(df['FRI'] == 1) & (df['SAT'] != 1)]
    saturday = df[(df['SAT'] == 1) & (df['FRI'] != 1)]
    both = df[(df['FRI'] == 1) & (df['SAT'] == 1)]

    final = pd.concat([
        friday.assign(ملاحظة="مداوم يوم الجمعة فقط"),
        saturday.assign(ملاحظة="مداوم يوم السبت فقط"),
        both.assign(ملاحظة="مداوم الجمعة والسبت")
    ])

    st.subheader("📍 قائمة الموظفين الخاصة:")
    st.dataframe(final[["EMP#", "ID#", "NAME (ENG)", "NAME (AR)", "FRI", "SAT", "ملاحظة"]].style.set_properties(**{
        'background-color': '#fdf6ec',
        'font-size': '13px'
    }), use_container_width=True)
