import os
import requests
import shutil
import zipfile

# KONFİQURASİYA
QRADAR_IP = "18.232.154.72"
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
TEMPLATE_ZIP = "rules/qradar/template.zip"
RULES_DIR = "rules/qradar/"

def deploy_to_qradar():
    print("🚀 Deploy prosesi başlayır...")
    
    # 1. Şablonu kopyalayırıq
    new_zip_name = "deploy_package.zip"
    shutil.copy(TEMPLATE_ZIP, new_zip_name)
    
    # 2. JSON fayllarını ZIP-ə əlavə edirik (QRadar-ın tanıması üçün)
    with zipfile.ZipFile(new_zip_name, 'a') as zipf:
        for file in os.listdir(RULES_DIR):
            if file.endswith(".json"):
                zipf.write(os.path.join(RULES_DIR, file), file)
    
    # 3. API-yə Göndər
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    headers = {'SEC': SEC_TOKEN, 'Accept': 'application/json'}
    
    print(f"📦 {new_zip_name} paketi QRadar-a göndərilir...")
    
    try:
        with open(new_zip_name, 'rb') as f:
            response = requests.post(url, headers=headers, files={'file': f}, verify=False)
            
        if response.status_code in [200, 201, 202]:
            print("✅ UĞURLU: Qayda paketi QRadar-a yükləndi!")
        else:
            print(f"❌ XƏTA {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Bağlantı xətası: {e}")

if __name__ == "__main__":
    deploy_to_qradar()
