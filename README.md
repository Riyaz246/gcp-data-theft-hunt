# Google Cloud "BigQuery Data Theft Hunt" Project

This project demonstrates my ability to perform data-driven threat hunting in a cloud environment. The scenario involved detecting a compromised VM that was using its over-privileged permissions to steal sensitive data from a Cloud Storage bucket.

This project moves beyond simple "prevention" (like firewall rules) and into active "detection and response."

## Skills Demonstrated
* **Advanced Log Configuration:** Enabled the critical, non-default **Cloud Storage Data Access Audit Logs** to capture "Data Read" events.
* **Data Engineering for Security:** Created a **Log Sink** to route specific, high-priority `data_access` logs from Cloud Logging into **BigQuery** for large-scale analysis.
* **Data-Driven Threat Hunting (BigQuery):** Wrote a **SQL query** to "hunt" for evidence of the attack, successfully identifying the data theft event from the raw logs.
* **Real-time Detection:** Built a **Cloud Monitoring Alert** to create a real-time detection rule that fires on the specific log entry for data theft.

---

## The "Attack" and "Detection" Process

### 1. Enabling Critical Log Sources
To detect data theft, I first had to enable the **Data Access Logs** for Cloud Storage, which are not on by default. This ensures every "read" event is recorded.

![Data Access Logs enabled for Cloud Storage](Screenshot%20(3).png)

### 2. Simulating the Attack
I simulated an attacker by SSH-ing into an "insecure" VM and using `gsutil` to discover and steal a file from a sensitive bucket.

![Terminal showing the gsutil cp command](Screenshot%20(11).png)

### 3. The Detection Engine: Sinking Logs to BigQuery
I created a log sink to route all `cloudaudit.googleapis.com/data_access` logs into a dedicated BigQuery dataset named `security_logs`.

![BigQuery dataset with the data_access table](Screenshot%20(12).png)

### 4. The Hunt: Finding the Data Theft
Using SQL, I queried the `data_access` log table. This query successfully identified the exact log entry where the `attacker-vm`'s service account called the `storage.objects.get` method on my sensitive file.

![BigQuery query and results for the data theft](Screenshot%20(13).png)

### 5. Automated Response: Real-Time Alert
Finally, I created a log-based alert in Cloud Monitoring that will notify me via email the *moment* a `storage.objects.get` event is logged in the future.

![The active Cloud Monitoring alert policy](Screenshot%20(14).png)

## Conclusion
This project demonstrates an end-to-end detection and response workflow. I successfully (1) instrumented a cloud environment to capture the right data, (2) aggregated and stored that data at scale in BigQuery, (3) hunted for the threat using SQL, and (4) built an automated alert for future incidents.
