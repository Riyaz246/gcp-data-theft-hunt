# 🤖 AI-Powered Threat Hunting Pipeline (A "GenAI-SIEM" Blueprint)

This project blueprint demonstrates a complete, end-to-end "GenAI-SIEM" pipeline.

It shows how to move beyond simple, noisy alerts by using BigQuery for large-scale log analysis and then feeding the results to the Vertex AI API to automate triage, summarize threats, and provide actionable remediation steps.

This solution is designed to solve the core **"alert fatigue"** problem in modern security operations.

---

## Skills Demonstrated

* **AI-Powered Triage (GenAI):** Using the Vertex AI API and advanced prompt engineering to automate incident summarization and reporting.
* **Serverless Automation:** Architecting an event-driven workflow (Pub/Sub, Cloud Functions) for a "zero-to-il" automated response.
* **Data Engineering for Security:** Creating a Log Sink to route high-priority `data_access` logs from Cloud Logging into BigQuery for large-scale analysis.
* **Data-Driven Threat Hunting (BigQuery):** Writing SQL queries to "hunt" for evidence of specific attacker TTPs (Tactics, Techniques, and Procedures).
* **Advanced Log Configuration:** Enabling the critical, non-default Cloud Storage Data Access Audit Logs.

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

### 6. The 'GenAI-SIEM' Upgrade (The AI-Powered Analyst)
A complete detection pipeline is great, but the real problem in SecOps is 'alert fatigue'. I wanted to show how to solve that, so I upgraded the final step with Generative AI.

This addition turns the project into a 'GenAI-SIEM'. Instead of just sending another basic, noisy alert, the pipeline now triggers the ai_triage.py script (which you can see in this repo).

This script is basically the 'brains' of the upgrade. It's simple but powerful:

1. It takes the raw, complex JSON log that the alert is based on.
2. It uses a custom prompt I engineered specifically for a security analyst.
3. It feeds both the log and the prompt to the Vertex AI API.

The result is a clean, human-readable report—not a raw log. It explains the threat clearly and even gives actionable remediation steps, which is what an analyst actually needs.

## Conclusion
This project shows the complete, end-to-end pipeline for a modern 'GenAI-SIEM'. I successfully:

1. ​Instrumented the GCP environment to capture the critical (and often-missed) Data Access Logs.
2. ​Engineered a data pipeline to sink those logs into BigQuery, creating a cost-effective 'Security Data Lake' for large-scale analysis.
3. ​Hunted for the specific data theft event at scale using SQL.
4. ​And most importantly: I built the AI-powered final step (the ai_triage.py script) that uses the Vertex AI API to solve the 'alert fatigue' problem.

​This pipeline doesn't just 'create another alert'. It automates the triage, analysis, and reporting, delivering a human-readable summary with actionable remediation steps. This proves I can build security solutions on GCP that are not only cost-effective and scalable but also genuinely intelligent.



```mermaid
graph TD
    subgraph GCP Environment
        Bucket[Cloud Storage Bucket] -- 1. Generates Data Access Logs --> Logging[Cloud Logging]
        Logging -- 2. Log Sink Routes Logs --> BigQuery[BigQuery Dataset (security_logs)]
        Bucket -- 3. Attacker Action (gsutil cp) --> Logging
    end

subgraph GenAI-SIEM Workflow
    %% This part is automated. The analyst is the *recipient* %%
    Monitoring[Cloud Monitoring (Log-based Alert)] -- 4. Continuously Monitors --> BigQuery
    Monitoring -- 5. Triggers on Match --> PubSub[Cloud Pub/Sub (Alert Topic)]
    PubSub -- 6. Triggers AI Triage --> Function[Cloud Function (ai_triage.py)]
    Function -- 7. Queries for Raw Log --> BigQuery
    Function -- 8. Sends Log to AI --> VertexAI[Vertex AI API]
    VertexAI -- 9. Returns Summary --> Function
    Function -- 10. Sends AI-Powered Alert --> Notify[Analyst (via Email/Slack)]
end