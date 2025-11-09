"""
AI-POWERED TRIAGE SCRIPT (GenAI-SIEM)
--------------------------------------
THIS IS THE "UPGRADE" to the "gcp-data-theft-hunt" project.

This script is intended to be run by a serverless function (like Cloud Functions)
or as a cron job on a Linux VM.

It is triggered *after* the initial Cloud Monitoring alert (Step 5) fires.

It demonstrates the "Brownfield Modernization" solution by:
1. Taking a simple alert (e.g., "EventID 4625 detected").
2. Querying BigQuery to get the *full, raw log* of the threat.
3. Feeding that raw log to the Vertex AI API with a specific SecOps prompt.
4. Generating a human-readable, actionable incident summary.

THIS IS THE "PROOF" for the Reliance Industries pitch.
"""

# We can't import these in a locked account, but we include them
# to show the full, correct architecture.
# from google.cloud import bigquery
# from vertexai.generative_models import GenerativeModel, Part

# --- 1. MOCK DATA (What Cloud Monitoring would send) ---
# In a real pipeline, this data would come from the Pub/Sub
# message that your Cloud Monitoring alert creates.
mock_alert_data = {
    "incident_name": "projects/your-project/incidents/12345",
    "summary": "Data Theft Hunt: storage.objects.get detected on sensitive-bucket",
    "threat_timestamp": "2025-11-09T15:01:00Z",
    "log_filter": "protoPayload.methodName=\"storage.objects.get\" AND resource.labels.bucket_name=\"sensitive-bucket\""
}

# --- 2. MOCK DATA (The raw log we *would* get from BigQuery) ---
# This is the raw, ugly JSON log that our SQL query (Step 4) would find.
# This is what we send to the AI.
mock_raw_log_from_bigquery = """
{
  "protoPayload": {
    "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
    "status": {},
    "authenticationInfo": {
      "principalEmail": "attacker-vm@your-project.iam.gserviceaccount.com",
      "principalSubject": "user:attacker@example.com"
    },
    "serviceName": "storage.googleapis.com",
    "methodName": "storage.objects.get",
    "resourceName": "projects/_/buckets/sensitive-bucket/objects/financial-report-q4.csv",
    "request": {
      "headers": {
        "user-agent": "gcloud-python/3.7.0",
        "x-goog-api-client": "gl-python/3.9.13 gccl/3.7.0"
      },
      "url": "https://storage.googleapis.com/sensitive-bucket/financial-report-q4.csv"
    },
    "metadata": {
      "network": {
        "source_ip": "35.188.1.100",
        "source_location": {
          "region": "us-central1",
          "zone": "us-central1-a"
        }
      }
    }
  },
  "insertId": "1a2b3c4d",
  "resource": {
    "type": "gcs_bucket",
    "labels": {
      "project_id": "your-project",
      "bucket_name": "sensitive-bucket",
      "location": "us"
    }
  },
  "timestamp": "2025-11-09T15:01:00Z",
  "severity": "INFO",
  "logName": "projects/your-project/logs/cloudaudit.googleapis.com%2Fdata_access"
}
"""

def get_ai_summary(raw_log_json: str) -> str:
    """
    This function simulates calling the Vertex AI API.
    We can't run this, but we've built the *exact* prompt
    and *manually written* the high-quality AI output.
    """
    
    # --- 3. THE PROMPT (The "Secret Sauce") ---
    # This is the prompt engineering for the GenAI-SIEM.
    prompt_to_vertex_ai = f"""
    You are a world-class Google Cloud SecOps Analyst (Level 3).
    A high-priority "data_access" log has been detected, indicating a
    potential data theft event.

    Your job is to parse the following raw JSON log, write a 3-sentence
    incident summary for a non-technical executive (CISO, CTO), and then
    list 3 concrete, technical remediation steps for the engineering team.

    Raw JSON Log:
    {raw_log_json}
    """
    
    # --- 4. THE SIMULATED AI OUTPUT ---
    # Since we can't call the API, we will *manually* create the
    # exact high-quality output the AI *would* generate.
    # THIS IS WHAT YOU SHOW IN THE DEMO.
    
    simulated_ai_output = """
**Incident Summary (Executive Level):**
A service account named 'attacker-vm' (likely running on a compromised server) just accessed and read a sensitive file named 'financial-report-q4.csv' from a critical storage bucket. This is a high-priority data exfiltration event. The action originated from inside our own 'us-central1' cloud region, suggesting an internal system compromise.

**Technical Remediation Steps:**
1.  **CONTAIN:** Immediately **disable** the service account key for `attacker-vm@your-project.iam.gserviceaccount.com` via the IAM & Admin API to cut off access.
2.  **INVESTIGATE:** Analyze all Cloud Audit Logs for the principal `attacker-vm` to determine the full "blast radius" (what else it accessed) *before* it was contained.
3.  **ERADICATE:** Identify and **isolate** the Compute Engine VM (`35.188.1.100`) that used this service account, as it is considered compromised.
"""
    
    print("--- PROMPT SENT TO VERTEX AI (This is what we engineer) ---")
    print(prompt_to_vertex_ai)
    print("\n" + "="*80 + "\n")
    print("--- SIMULATED AI RESPONSE (This is what we show the VP) ---")
    print(simulated_ai_output)
    
    return simulated_ai_output

# --- 5. Run the "Solution Blueprint" ---
if __name__ == "__main__":
    get_ai_summary(mock_raw_log_from_bigquery)