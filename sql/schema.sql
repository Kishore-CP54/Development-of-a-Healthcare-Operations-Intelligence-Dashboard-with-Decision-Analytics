CREATE TABLE healthcare_operations (
date DATE NOT NULL,
department VARCHAR(100) NOT NULL,
admissions INTEGER,
discharges INTEGER,
emergency_cases INTEGER,
available_beds INTEGER,
occupied_beds INTEGER,
bed_utilization DECIMAL(6,2),
staff_count INTEGER,
staff_utilization DECIMAL(6,2),
equipment_utilization DECIMAL(6,2),
average_los DECIMAL(6,2),
treatment_demand INTEGER
);