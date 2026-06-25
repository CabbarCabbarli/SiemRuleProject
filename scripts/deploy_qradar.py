import os
import json
import requests
import urllib3

# Təhlükəsizlik xəbərdarlığını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFİQURASİYA ---
QRADAR_IP = "18.232.154.72" 
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
RULES_DIR = 'rules/qradar' # Faylların olduğu qovluq
# ---------------------

def deploy_rule(file_path):
    # Faylı oxuyuruq
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            # Faylın JSON olduğundan əmin olmalısan
            rule_data = json.load(f)
        except Exception as e:
            print(f"XƏTA: Fayl JSON formatında deyil! -> {e}")
            return

    # QRadar API Endpoint (POST)
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    headers = {
        'SEC': SEC_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Version': '12.0'
    }
    
    print(f"İşlənir: {rule_data.get('name')}...")
    
    try:
        response = requests.post(url, json=rule_data, headers=headers, verify=False, timeout=15)
        
        if response.status_code in [200, 201]:
            print(f"✅ UĞURLU: {rule_data.get('name')} yaradıldı.")
        else:
            print(f"❌ XƏTA {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Bağlantı xətası: {e}")

def main():
    if not os.path.exists(RULES_DIR):
        print(f"XƏTA: {RULES_DIR} qovluğu tapılmadı!")
        return
        
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            deploy_rule(os.path.join(RULES_DIR, filename))

if __name__ == "__main__":
    main()
