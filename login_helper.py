import json

def parse_cookie_string(cookie_str):
    cookies = []
    pairs = cookie_str.strip().strip("'").strip('"').split(';')
    for pair in pairs:
        if '=' not in pair:
            continue
        idx = pair.find('=')
        name = pair[:idx].strip()
        value = pair[idx+1:].strip()
        cookies.append({
            "name": name,
            "value": value,
            "domain": ".1688.com",
            "path": "/",
            "expires": -1,
            "httpOnly": False,
            "secure": False,
            "sameSite": "Lax"
        })
    return cookies

def login_and_save_state():
    print("=========================================")
    print("1688 쿠키 수동 등록 도우미 (봇 탐지 회피)")
    print("=========================================")
    print("※ (중요) 기존 document.cookie 명령어 방식은 보안 쿠키가 누락되어 로그인이 안 됩니다.")
    print("1. 평소 쓰시는 Chrome 브라우저로 1688.com 에 접속 후 로그인 상태를 확인하세요.")
    print("2. 키보드 [F12]를 눌러 개발자 도구를 열고, 상단 [Network(네트워크)] 탭을 클릭하세요.")
    print("3. 브라우저 새로고침(F5)을 한 번 해주세요.")
    print("4. 아래 뜨는 목록 목록 중 맨 위쪽의 파일(예: www.1688.com)을 클릭하세요.")
    print("5. 우측 창의 스크롤을 내려 [Request Headers(요청 헤더)]라는 영역을 찾으세요.")
    print("6. 'cookie:' 항목을 찾아 그 옆에 아주 길게 적힌 텍스트를 우클릭 후 'Copy value(값 복사)'를 누르세요.")
    print("\n-----------------------------------------")
    print("복사한 쿠키 전체를 아래에 붙여넣고 엔터키를 눌러주세요:")
    
    cookie_str = input("\n[여기에 붙여넣기]: ")
    
    if not cookie_str or "=" not in cookie_str:
        print("올바른 쿠키 문자열이 아닙니다. 잠시 후 다시 실행해주세요.")
        return
        
    cookies = parse_cookie_string(cookie_str)
    state = {
        "cookies": cookies,
        "origins": []
    }
    
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        
    print(f"\n✅ 성공! 총 {len(cookies)}개의 쿠키 정보가 state.json 파일에 저장되었습니다.")
    print("이제 봇이 일반 웹 브라우저의 접속 권한을 사용하여 안정적으로 스크래핑합니다.")

if __name__ == "__main__":
    login_and_save_state()
