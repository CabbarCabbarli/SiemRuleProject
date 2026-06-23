import os
import yaml
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_HOST = os.getenv('SPLUNK_HOST')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN')
RULES_DIR = 'rules/splunk'

def deploy_rule(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            rule = yaml.safe_load(f)
        except Exception as e:
            print(f"YAML oxunma xətası: {e}")
            return

    url = f"{SPLUNK_HOST}/servicesNS/msplunk/search/saved/searches""
    headers = {'Authorization': f'Splunk {SPLUNK_TOKEN}'}
    
    payload = {
        'name': rule['title'],
        'search': rule['detection']['condition'],
        'description': rule.get('description', 'No description'),
        'is_scheduled': 1,
        'cron_schedule': '*/5 * * * *'
    }

    try:
        response = requests.post(url, data=payload, headers=headers, verify=False, timeout=10)
        if response.status_code in [200, 201]:
            print(f"OK: {rule['title']} uğurla yaradıldı.")
        else:
            print(f"XƏTA {response.status_code}: {rule['title']} -> {response.text}")
    except Exception as e:
        print(f"Bağlantı xətası (Serverə çata bilmirəm): {e}")

def main():
    if not SPLUNK_HOST or not SPLUNK_TOKEN:
        print("XƏTA: SPLUNK_HOST və ya SPLUNK_TOKEN mühit dəyişənləri tapılmadı!")
        return
        
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".yaml"):
            deploy_rule(os.path.join(RULES_DIR, filename))

if __name__ == "__main__":
    main()
