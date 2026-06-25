import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfiqurasiya
QRADAR_IP = "18.232.154.72" 
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
RULES_DIR = '../rules/qradar' 

def deploy_rule(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            # QRadar JSON gözləyir, YAML yox. Faylların JSON olduğundan əmin ol.
            rule = json.load(f) 
        except Exception as e:
            print(f"JSON oxunma xətası: {e}")
            return

    # QRadar üçün ən vacib endpoint
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    headers = {
        'SEC': SEC_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Version': '12.0' # Versiyanı mütləq qeyd etməliyik
    }
    
    try:
        # payload artıq faylın içindəki JSON-dur
        response = requests.post(url, json=rule, headers=headers, verify=False, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"OK: {rule.get('name')} uğurla yaradıldı.")
        else:
            print(f"XƏTA {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Bağlantı xətası: {e}")

def main():
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            deploy_rule(os.path.join(RULES_DIR, filename))

if __name__ == "__main__":
    main()
