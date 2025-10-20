-- This query hunts for Cloud Storage data read events (potential theft)
-- originating from a specific VM identified as 'attacker-vm'.
-- It uses the Data Access audit logs sinked to BigQuery.

SELECT
  timestamp,                                  -- When the event occurred
  principalEmail,                             -- Who performed the action (Service Account email)
  protopayload_auditlog.methodName,           -- The specific API method called (should be storage.objects.get)
  protopayload_auditlog.resourceName          -- The file that was accessed (e.g., gs://bucket/file.txt)
FROM
  -- !!! --- EDIT THIS TABLE NAME --- !!!
  `threat-hunting-project.security_logs.cloudaudit_googleapis_com_data_access_20251018` -- Replace with your actual table name
WHERE
  -- Filter for the specific data read method
  protopayload_auditlog.methodName = "storage.objects.get"
ORDER BY
  -- Show the most recent events first
  timestamp DESC
LIMIT 10 -- Limit results for brevity
