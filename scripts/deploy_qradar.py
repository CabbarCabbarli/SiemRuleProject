import os
import requests
import zipfile
import shutil

# KONFİQURASİYA
QRADAR_IP = "18.232.154.72"
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
TEMPLATE_ZIP = "rules/qradar/template.zip"
RULES_DIR = "rules/"

def deploy_to_qradar():
    print("🚀 ZIP Paketləmə və Deploy başlayır...")
    
    # 1. ZIP-i hazırla
    new_zip_name = "final_rule_package.zip"
    shutil.copy(TEMPLATE_ZIP, new_zip_name) # Şablonu kopyalayırıq
    
    with zipfile.ZipFile(new_zip_name, 'a') as zipf:
        # JSON faylını ZIP-in içinə əlavə edirik (QRadar-ın gözlədiyi yola)
        zipf.write(os.path.join(RULES_DIR, "rule1.json"), "rule1.json")
    
    # 2. API-yə Göndər
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    headers = {'SEC': SEC_TOKEN}
    
    print("📦 Paket QRadar-a göndərilir...")
    with open(new_zip_name, 'rb') as f:
        response = requests.post(url, headers=headers, files={'file': f}, verify=False)
        
    if response.status_code in [200, 201, 202]:
        print("✅ UĞURLU: Qayda paketi yükləndi!")
    else:
        print(f"❌ XƏTA {response.status_code}: {response.text}")

if __name__ == "__main__":
    deploy_to_qradar()
