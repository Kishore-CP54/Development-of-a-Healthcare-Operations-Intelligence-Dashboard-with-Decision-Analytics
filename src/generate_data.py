from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)
departments={"Emergency":(45,28,55),"Cardiology":(35,24,38),"Neurology":(30,20,32),"Orthopedics":(40,22,42),"General Medicine":(55,30,60),"Pediatrics":(30,21,35)}
dates=pd.date_range("2026-01-01","2026-03-31",freq="D")
rows=[]

for date in dates:
    factor=1.12 if date.dayofweek<5 else .92
    for dept,(beds,staff,demand) in departments.items():
        admissions=max(5,int(np.random.normal(demand*factor,demand*.12)))
        if date.day in [10,11,12] and dept in ["Emergency","General Medicine"]:
            admissions=int(admissions*1.25)
        discharges=max(3,int(np.random.normal(admissions*.88,3)))
        occupied=min(beds,max(1,int(np.random.normal(admissions*.82,3))))
        bed_util=round(occupied/beds*100,2)
        staff_util=round(min(100,max(35,np.random.normal(62+admissions/demand*22,7))),2)
        equipment_util=round(min(100,max(25,np.random.normal(58+admissions/demand*18,8))),2)
        emergency=max(0,int(np.random.normal(admissions*(.34 if dept=="Emergency" else .08),2)))
        los=round(max(1,np.random.normal({"Emergency":2.2,"Cardiology":5.1,"Neurology":4.6,"Orthopedics":5.8,"General Medicine":4,"Pediatrics":3.1}[dept],.7)),2)
        rows.append([date,dept,admissions,discharges,emergency,beds,occupied,bed_util,staff,staff_util,equipment_util,los,int(np.random.normal(admissions*1.25,5))])

cols=["date","department","admissions","discharges","emergency_cases","available_beds","occupied_beds","bed_utilization","staff_count","staff_utilization","equipment_utilization","average_los","treatment_demand"]
out=pd.DataFrame(rows,columns=cols)
Path("data").mkdir(exist_ok=True)
out.to_csv("data/healthcare_operations.csv",index=False)
print(f"Generated {len(out)} records.")
