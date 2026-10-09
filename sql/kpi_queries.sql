SELECT department, SUM(admissions) AS total_admissions
FROM healthcare_operations GROUP BY department ORDER BY total_admissions DESC;

SELECT ROUND(AVG(bed_utilization),2) AS avg_bed_utilization
FROM healthcare_operations;

SELECT date, SUM(admissions) AS admissions, SUM(discharges) AS discharges
FROM healthcare_operations GROUP BY date ORDER BY date;

SELECT date, department, staff_utilization
FROM healthcare_operations WHERE staff_utilization >= 90
ORDER BY date, department;