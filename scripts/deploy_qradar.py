import os
import requests
import urllib3
import time

# QRadar-ın öz-özünə imzaladığı (self-signed) sertifikat xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFİQURASİYA BÖLMƏSİ ---
QRADAR_IP = "18.232.154.72" 
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
ZIP_FILE_PATH = "rules/qradar/qradar_rules.zip" # GitHub-da saxlayacağımız fayl
# -----------------------------

def deploy_rules_to_qradar():
    print(f"🚀 GitHub -> QRadar Avtomatlaşdırması Başlayır...")
    
    if not os.path.exists(ZIP_FILE_PATH):
        print(f"❌ XƏTA: Qayda paketi ({ZIP_FILE_PATH}) tapılmadı!")
        print("Məsləhət: QRadar-dan export etdiyiniz .zip faylını bu qovluğa qoyun.")
        return

    # QRadar Extension API endpointi
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    
    headers = {
        'SEC': SEC_TOKEN,
        'Accept': 'application/json'
    }
    
    print(f"📦 Paketlənmiş qaydalar oxunur və API-yə göndərilir...")
    
    try:
        # Faylı binary formatda oxuyub POST edirik
        with open(ZIP_FILE_PATH, 'rb') as f:
            files = {'file': (os.path.basename(ZIP_FILE_PATH), f, 'application/zip')}
            response = requests.post(url, headers=headers, files=files, verify=False, timeout=30)
            
        if response.status_code in [200, 201, 202]:
            print("✅ UĞURLU: Qaydalar QRadar-a müvəffəqiyyətlə transfer edildi!")
            task_info = response.json()
            print(f"Status: {task_info.get('status', 'Bilinmir')}")
            print(f"Bu əməliyyatla SİEM-də qaydalar güncəlləndi.") [cite: 151]
        else:
            print(f"❌ API XƏTASI {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ XƏTA: QRadar serverinə qoşulmaq mümkün olmadı. IP və ya VPN-i yoxlayın.")
    except Exception as e:
        print(f"Gözlənilməz xəta: {e}")

if __name__ == "__main__":
    deploy_rules_to_qradar()
