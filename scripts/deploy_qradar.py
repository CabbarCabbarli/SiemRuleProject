import os
import json
import requests
import urllib3

# Təhlükəsizlik xəbərdarlıqlarını (SSL) söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFİQURASİYA BÖLMƏSİ ---
QRADAR_IP = "18.232.154.72" 
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
RULES_DIR = "rules/qradar/" # JSON fayllarının olduğu qovluq
# -----------------------------

def deploy_json_rules():
    print("🚀 GitHub JSON -> QRadar API birbaşa atəşləmə başlayır...")
    
    # DOĞRU API YOLU (Endpoint) budur!
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    headers = {
        'SEC': SEC_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if not os.path.exists(RULES_DIR):
        print(f"❌ XƏTA: {RULES_DIR} qovluğu tapılmadı!")
        return

    # Qovluqdakı bütün json fayllarını tapırıq
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(RULES_DIR, filename)
            
            # Faylı oxuyuruq
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    rule_payload = json.load(f)
                except Exception as e:
                    print(f"⚠️ {filename} oxunarkən xəta (JSON formatı səhvdir): {e}")
                    continue
            
            print(f"📦 Göndərilir: {filename}...")
            
            # API-yə POST sorğusu göndəririk
            response = requests.post(url, headers=headers, json=rule_payload, verify=False, timeout=30)
            
            # QRadar 201 (Created) qaytarırsa, qayda uğurla yaradılıb
            if response.status_code in [201, 200, 202]:
                print(f"✅ UĞURLU: {filename} QRadar-a yazıldı!")
            else:
                print(f"❌ XƏTA {response.status_code} ({filename}): {response.text}")

if __name__ == "__main__":
    deploy_json_rules()
