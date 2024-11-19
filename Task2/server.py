import socket  # 소켓 통신을 위한 표준 라이브러리
import threading  # 멀티스레딩 처리를 위한 라이브러리
from datetime import datetime  # 메시지에 시간 정보를 추가하기 위한 라이브러리
import openai  # OpenAI API 사용을 위한 라이브러리

# OpenAI API 키 설정
openai.api_key = '개인 OpenAI API Key이라 이는 따로 제거하였습니다. 참고 바랍니다.'

# 서버 설정
HOST = '127.0.0.1'  # 서버 IP 주소 (로컬 테스트용)
PORT = 5002  # 사용할 포트 번호

# 클라이언트 정보를 저장하는 딕셔너리: {클라이언트 소켓: 닉네임}
clients = {}

def broadcast(message, sender=None):
    """모든 클라이언트에게 메시지를 전송하는 함수
    - message: 전송할 메시지 (문자열)
    - sender: 메시지를 보낸 클라이언트 소켓 (해당 클라이언트를 제외하고 전송)
    """
    for client, nickname in clients.items():
        if client != sender:  # 메시지 보낸 클라이언트는 제외
            client.sendall(message.encode())  # 메시지를 UTF-8로 인코딩하여 전송

def format_message(nickname, message):
    """메시지 포맷팅 함수
    - nickname: 메시지를 보낸 사용자의 닉네임
    - message: 전송할 메시지 내용
    - 반환값: 닉네임과 시간 정보가 추가된 포맷된 메시지
    """
    current_time = datetime.now().strftime("%H:%M:%S")  # 현재 시간을 HH:MM:SS 형식으로 가져오기
    return f"[{current_time}] {nickname}: {message}"  # 포맷된 메시지 반환

def search_openai(query):
    """OpenAI API를 사용해 GPT-4 기반 검색 결과 반환
    - query: 사용자가 입력한 검색어
    - 반환값: OpenAI API의 응답 텍스트
    """
    try:
        # OpenAI ChatCompletion API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 최신 GPT-4 모델 사용
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # 시스템 역할 설정
                {"role": "user", "content": query}  # 사용자 입력 설정
            ],
            max_tokens=500,  # 출력될 최대 토큰 수 제한
            temperature=0.7  # 출력 다양성 설정 (값이 높을수록 창의적인 응답)
        )
        # OpenAI 응답에서 텍스트 추출
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        # API 호출 중 오류 발생 시 오류 메시지 반환
        return f"검색 중 오류 발생: {e}"

def handle_client(conn, addr):
    """클라이언트와의 연결을 처리하는 함수
    - conn: 클라이언트 소켓 객체
    - addr: 클라이언트의 주소 정보
    """
    # 클라이언트에게 닉네임 입력 요청
    conn.sendall("닉네임을 입력하세요: ".encode())
    nickname = conn.recv(1024).decode()  # 클라이언트로부터 닉네임 수신
    clients[conn] = nickname  # 닉네임과 클라이언트 소켓을 딕셔너리에 저장
    print(f"{nickname}({addr}) 연결됨.")  # 서버 측에 연결 로그 출력
    broadcast(f"{nickname} 님이 채팅방에 참여했습니다.")  # 다른 클라이언트에게 참여 메시지 전송

    try:
        while True:
            message = conn.recv(1024).decode()  # 클라이언트로부터 메시지 수신
            if message.startswith("/"):  # 명령어 처리
                if message == "/exit":  # 연결 종료 명령어
                    conn.sendall("연결을 종료합니다.".encode())  # 클라이언트에게 종료 메시지 전송
                    break  # 연결 종료
                elif message == "/users":  # 접속자 목록 요청
                    user_list = ", ".join(clients.values())  # 현재 접속 중인 닉네임 목록 생성
                    conn.sendall(f"접속자 목록: {user_list}".encode())  # 목록 전송
                elif message.startswith("/search "):  # OpenAI 검색 명령어
                    query = message.split(" ", 1)[1]  # 검색어 추출
                    result = search_openai(query)  # OpenAI API 호출
                    # 검색 결과를 모든 클라이언트에게 브로드캐스트
                    broadcast(f"{nickname}님의 검색 결과:\n{result}")
                elif message.startswith("/nick "):  # 닉네임 변경 명령어
                    new_nickname = message.split(" ", 1)[1]  # 새 닉네임 추출
                    old_nickname = clients[conn]  # 기존 닉네임 가져오기
                    if new_nickname in clients.values():  # 중복 닉네임 검사
                        conn.sendall("이미 사용 중인 닉네임입니다.".encode())  # 중복 닉네임 경고
                    else:
                        clients[conn] = new_nickname  # 닉네임 변경
                        broadcast(f"{old_nickname} 님이 닉네임을 {new_nickname}(으)로 변경했습니다.")
                        conn.sendall(f"닉네임이 {new_nickname}(으)로 변경되었습니다.".encode())
                elif message == "/help":  # 명령어 목록 요청
                    help_message = (
                        "사용 가능한 명령어:\n"
                        "/help - 명령어 목록 표시\n"
                        "/exit - 채팅방 나가기\n"
                        "/users - 접속자 목록 보기\n"
                        "/nick [새 닉네임] - 닉네임 변경\n"
                        "/search [내용] - OpenAI 기반 검색"
                    )
                    conn.sendall(help_message.encode())  # 명령어 목록 전송
                else:
                    conn.sendall("알 수 없는 명령어입니다.".encode())  # 알 수 없는 명령어 경고
            else:
                # 일반 메시지 처리: 메시지를 브로드캐스트
                broadcast(format_message(nickname, message), sender=conn)
    finally:
        # 클라이언트 연결 종료 처리
        broadcast(f"{clients[conn]} 님이 채팅방을 떠났습니다.")  # 다른 클라이언트에게 연결 종료 알림
        del clients[conn]  # 딕셔너리에서 클라이언트 제거
        conn.close()  # 클라이언트 소켓 닫기

# 메인 서버 실행
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓 생성
server_socket.bind((HOST, PORT))  # IP 주소와 포트를 소켓에 바인딩
server_socket.listen(5)  # 최대 5개 클라이언트 연결 대기
print(f"서버가 {HOST}:{PORT}에서 대기 중입니다...")

try:
    while True:
        conn, addr = server_socket.accept()  # 클라이언트 연결 요청 수락
        threading.Thread(target=handle_client, args=(conn, addr)).start()  # 클라이언트 처리 스레드 실행
finally:
    server_socket.close()  # 서버 소켓 닫기
