import os
import requests
import urllib3

# Təhlükəsizlik (SSL) xəbərdarlıqlarını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFİQURASİYA ---
QRADAR_IP = "18.232.154.72" 
SEC_TOKEN = "74a7852b-2e30-42e7-9f78-66824ed6f764"
ZIP_FILE_PATH = "rules/qradar/qradar_rules.zip" # ZIP faylının olacağı yol
# ---------------------

def upload_zip_to_qradar(file_path):
    if not os.path.exists(file_path):
        print(f"❌ XƏTA: {file_path} tapılmadı! Zəhmət olmasa ZIP faylını ora yerləşdirin.")
        return

    # QRadar-ın Rəsmi ZIP (Extension) qəbul edən API qapısı
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    
    headers = {
        'SEC': SEC_TOKEN,
        'Accept': 'application/json'
        # Qeyd: 'Content-Type' requests tərəfindən 'multipart/form-data' olaraq avtomatik təyin ediləcək
    }
    
    print(f"🚀 Atəşləmə Başlayır: {file_path} QRadar-a yüklənir...")
    
    try:
        # Faylı binary (rb) rejimində oxuyuruq və göndəririk
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/zip')}
            response = requests.post(url, headers=headers, files=files, verify=False, timeout=30)
            
        if response.status_code in [200, 201, 202]:
            print("✅ UĞURLU: ZIP faylı QRadar-a tam yükləndi!")
            # QRadar cavab olaraq extension_id verəcək
            print(f"QRadar Cavabı: {response.json().get('status', 'Gözləyir...')}")
        else:
            print(f"❌ XƏTA {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı xətası: {e}")

if __name__ == "__main__":
    upload_zip_to_qradar(ZIP_FILE_PATH)
