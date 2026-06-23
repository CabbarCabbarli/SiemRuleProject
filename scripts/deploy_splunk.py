import os
import yaml
import requests
import urllib3

# Təhlükəsizlik xəbərdarlığı: SSL xətalarını görməmək üçün (əgər self-signed sertifikatdırsa)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub Secrets-dən dəyişənləri alırıq
SPLUNK_HOST = os.getenv('SPLUNK_HOST')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN')

# Qaydaların yerləşdiyi qovluq
RULES_DIR = 'rules/splunk'

def deploy_rule(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        rule = yaml.safe_load(f)

    # Splunk API Endpoint (Saved Searches üçün)
    url = f"{SPLUNK_HOST}/services/saved/searches"
    
    # Payload (Splunk-ın tələb etdiyi format)
    payload = {
        'name': rule['title'],
        'search': rule['detection']['condition'],
        'description': rule.get('description', ''),
        'is_scheduled': 1,
        'cron_schedule': '*/5 * * * *', # Hər 5 dəqiqədən bir işləsin
        'dispatch.earliest_time': '-1h',
        'dispatch.latest_time': 'now'
    }

    headers = {'Authorization': f'Splunk {SPLUNK_TOKEN}'}

    # API-yə göndərmə
    response = requests.post(url, data=payload, headers=headers, verify=False)
    
    if response.status_code in [200, 201]:
        print(f"OK: {rule['title']} uğurla yayımlandı.")
    else:
        print(f"XƏTA: {rule['title']} göndərilə bilmədi. Status: {response.status_code}, Cavab: {response.text}")

def main():
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".yaml"):
            file_path = os.path.join(RULES_DIR, filename)
            deploy_rule(file_path)

if __name__ == "__main__":
    main()
