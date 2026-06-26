import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = "18.232.154.72"
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"

# GitHub-dakı təmiz JSON qayda faylımız
JSON_RULE_PATH = "rules/qradar/rule1.json"

# Bayaq QRadar-da yaratdığın o qaydanın ID-si (Məsələn: 100054 və s.)
# Siyahıdakı hər hansı bir sistem qaydasının ID-si ilə də test edə bilərsən
RULE_ID = "100054" 

def deploy_pure_json_rule():
    print(f"🚀 GitHub-dakı JSON qayda faylı oxunur: {JSON_RULE_PATH}")
    
    # 1. GitHub-dakı JSON-u oxuyuruq
    with open(JSON_RULE_PATH, "r", encoding="utf-8") as f:
        rule_data = json.load(f)
        
    # 2. Müəllimin dediyi o birbaşa qayda yeniləmə API endpointi (PUT metodu)
    url = f"https://{QRADAR_IP}/api/config/extension_management/extension{RULE_ID}"
    headers = {
        'SEC': SEC_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print(f"📡 Qayda məntiqi API (PUT) vasitəsilə QRadar-a PUSH edilir...")
    
    # Heç bir ZIP olmadan, təmiz JSON datası göndərilir!
    response = requests.put(url, headers=headers, json=rule_data, verify=False)
    
    if response.status_code in [200, 201, 204]:
        print(f"🎉 UĞURLU! Qayda GitHub-dakı məlumatlar əsasında tam avtomatik olaraq QRadar-da yeniləndi!")
        print(f"👉 Yenilənən Qayda: {rule_data['name']}")
    else:
        print(f"❌ XƏTA: {response.status_code} - {response.text}")

if __name__ == "__main__":
    deploy_pure_json_rule()
