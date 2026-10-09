import pandas as pd

def calculate_kpis(df):
    return {
        "admissions": int(df.admissions.sum()),
        "discharges": int(df.discharges.sum()),
        "bed_utilization": float(df.bed_utilization.mean()),
        "avg_los": float(df.average_los.mean()),
        "staff_utilization": float(df.staff_utilization.mean())
    }

def department_summary(df):
    return df.groupby("department",as_index=False).agg(
        admissions=("admissions","sum"),
        discharges=("discharges","sum"),
        bed_utilization=("bed_utilization","mean"),
        staff_utilization=("staff_utilization","mean"),
        average_los=("average_los","mean")
    ).sort_values("admissions",ascending=False)

def build_alerts(df):
    thresholds={"Emergency":55,"Cardiology":38,"Neurology":32,"Orthopedics":42,"General Medicine":60,"Pediatrics":35}
    rows=[]
    for _,r in df.iterrows():
        if r.bed_utilization>=90:
            rows.append({"date":r.date,"department":r.department,"severity":"High","alert":"Bed utilization is >= 90%","recommendation":"Review bed capacity and discharge/transfer planning."})
        if r.staff_utilization>=90:
            rows.append({"date":r.date,"department":r.department,"severity":"High","alert":"Staff utilization is >= 90%","recommendation":"Review staffing coverage and workload distribution."})
        if r.admissions>thresholds.get(r.department,999):
            rows.append({"date":r.date,"department":r.department,"severity":"Medium","alert":"Admissions exceed configured demand threshold","recommendation":"Monitor demand and evaluate resource readiness."})
    return pd.DataFrame(rows)
