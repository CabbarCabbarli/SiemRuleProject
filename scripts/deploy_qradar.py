import os
import json
import requests
import urllib3

# QRadar-ın self-signed sertifikat xətalarını gizlətmək üçün
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= KONFİQURASİYA =================
QRADAR_IP = "18.232.154.72"  # Məsələn: 217.25.27.174
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
RULES_DIR = "../rules/qradar" # Skript scripts qovluğunda olduğu üçün bir pillə geri qayıdırıq
# =================================================

HEADERS = {
    "SEC": SEC_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

API_URL = f"https://{QRADAR_IP}/api/analytics/rules"

def push_rules():
    print("🚀 QRadar API Push Əməliyyatı Başlayır...\n")
    
    # Qovluqdakı bütün json fayllarını tap
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RULES_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    rule_data = json.load(file)
                    rule_name = rule_data.get("name", filename)
                    
                    # API-yə göndər
                    response = requests.post(API_URL, headers=HEADERS, json=rule_data, verify=False)
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ UĞURLU: '{rule_name}' QRadar-a yazıldı!")
                    elif response.status_code == 409:
                        print(f"⚠️ MÖVCUDDUR: '{rule_name}' artıq QRadar-da var.")
                    else:
                        print(f"❌ XƏTA ({response.status_code}): '{rule_name}' yüklənmədi. Səbəb: {response.text}")
                        
                except Exception as e:
                    print(f"❌ Fayl oxunma xətası ({filename}): {e}")

if __name__ == "__main__":
    push_rules()
