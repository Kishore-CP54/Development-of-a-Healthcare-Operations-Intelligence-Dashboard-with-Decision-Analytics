import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.analytics import calculate_kpis, build_alerts, department_summary

st.set_page_config(page_title="Healthcare Operations Intelligence", page_icon="🏥", layout="wide")
st.title("🏥 Healthcare Operations Intelligence Dashboard")
st.caption("Operational monitoring, KPI analytics and decision support")

path = Path("data/healthcare_operations.csv")
if not path.exists():
    st.error("Dataset not found. Run: python src/generate_data.py")
    st.stop()

df = pd.read_csv(path, parse_dates=["date"])

st.sidebar.header("Filters")
dept = st.sidebar.selectbox("Department", ["All"] + sorted(df.department.unique()))
dates = st.sidebar.date_input("Date range", (df.date.min().date(), df.date.max().date()))

if isinstance(dates, tuple) and len(dates) == 2:
    start, end = dates
else:
    start = end = dates

d = df[(df.date.dt.date >= start) & (df.date.dt.date <= end)].copy()
if dept != "All":
    d = d[d.department == dept]

if d.empty:
    st.warning("No data for selected filters.")
    st.stop()

k = calculate_kpis(d)
a,b,c,e,f = st.columns(5)
a.metric("Admissions", f"{k['admissions']:,}")
b.metric("Discharges", f"{k['discharges']:,}")
c.metric("Bed Utilization", f"{k['bed_utilization']:.1f}%")
e.metric("Avg LOS", f"{k['avg_los']:.1f} days")
f.metric("Staff Utilization", f"{k['staff_utilization']:.1f}%")

t1,t2,t3,t4,t5 = st.tabs(["Overview","Patient Flow","Resources","Departments","Decision Analytics"])

with t1:
    daily = d.groupby("date",as_index=False).agg(admissions=("admissions","sum"),discharges=("discharges","sum"),bed_utilization=("bed_utilization","mean"))
    st.plotly_chart(px.line(daily,x="date",y=["admissions","discharges"],markers=True,title="Admissions vs Discharges"),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.plotly_chart(px.bar(department_summary(d),x="department",y="admissions",title="Admissions by Department"),use_container_width=True)
    with c2:
        st.plotly_chart(px.line(daily,x="date",y="bed_utilization",title="Bed Utilization Trend"),use_container_width=True)

with t2:
    flow=d.groupby("date",as_index=False).agg(admissions=("admissions","sum"),discharges=("discharges","sum"),emergency_cases=("emergency_cases","sum"))
    st.plotly_chart(px.line(flow,x="date",y=["admissions","discharges","emergency_cases"],markers=True,title="Patient Flow"),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.plotly_chart(px.bar(d.groupby("department",as_index=False).admissions.sum(),x="department",y="admissions",title="Admissions"),use_container_width=True)
    with c2:
        st.plotly_chart(px.box(d,x="department",y="average_los",title="Length of Stay"),use_container_width=True)

with t3:
    r=d.groupby("date",as_index=False).agg(available_beds=("available_beds","sum"),occupied_beds=("occupied_beds","sum"),bed_utilization=("bed_utilization","mean"),equipment_utilization=("equipment_utilization","mean"))
    st.plotly_chart(px.line(r,x="date",y=["available_beds","occupied_beds"],markers=True,title="Available vs Occupied Beds"),use_container_width=True)
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.area(r,x="date",y="bed_utilization",title="Bed Utilization"),use_container_width=True)
    with c2: st.plotly_chart(px.line(r,x="date",y="equipment_utilization",title="Equipment Utilization"),use_container_width=True)

with t4:
    summary=department_summary(d)
    st.plotly_chart(px.bar(summary,x="department",y=["admissions","staff_utilization"],barmode="group",title="Department Workload"),use_container_width=True)
    st.dataframe(summary,use_container_width=True)

with t5:
    st.subheader("Operational Alerts")
    alerts=build_alerts(d)
    if alerts.empty:
        st.success("No threshold-based alerts detected.")
    for _,r in alerts.iterrows():
        msg=f"**{r.department} — {r.date.date()}**: {r.alert}  
Recommendation: {r.recommendation}"
        if r.severity=="High": st.error(msg)
        else: st.warning(msg)
    st.info("Alerts are decision-support indicators, not clinical instructions.")

st.divider()
st.caption("Synthetic data for educational/internship demonstration only.")
