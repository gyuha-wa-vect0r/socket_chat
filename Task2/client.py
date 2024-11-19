import socket  # 소켓 통신을 위한 표준 라이브러리
import threading  # 멀티스레딩 처리를 위한 라이브러리

# 서버 연결 설정
HOST = '127.0.0.1'  # 서버의 IP 주소 (로컬호스트)
PORT = 5002  # 서버와 통신할 포트 번호

def receive_messages(sock):
    """
    서버로부터 메시지를 수신하는 함수.
    - 서버에서 메시지를 수신하여 클라이언트 화면에 출력.
    - 서버와 연결이 끊어질 경우 종료 메시지를 출력.
    - sock: 클라이언트와 연결된 소켓 객체.
    """
    while True:
        try:
            # 서버로부터 1024바이트 크기의 메시지 데이터를 수신
            message = sock.recv(1024).decode()
            # 수신된 메시지를 화면에 출력
            print(message)
        except:
            # 서버와 연결이 끊어진 경우 에러 메시지를 출력하고 소켓 종료
            print("서버와의 연결이 종료되었습니다.")
            sock.close()
            break

# 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결 요청
client_socket.connect((HOST, PORT))

# 서버로부터 초기 메시지(닉네임 요청)를 수신
initial_message = client_socket.recv(1024).decode()
print(initial_message)  # 서버로부터 받은 초기 메시지 출력

# 클라이언트 사용자 닉네임 입력
nickname = input()  # 사용자로부터 닉네임 입력
client_socket.sendall(nickname.encode())  # 입력받은 닉네임을 서버에 전송

# 서버로부터 메시지를 수신하는 스레드 시작
# - receive_messages 함수가 별도의 스레드에서 실행되어
#   서버 메시지를 비동기적으로 수신
threading.Thread(target=receive_messages, args=(client_socket,)).start()

try:
    while True:
        # 사용자로부터 메시지 입력 대기
        message = input()
        
        if message == "/exit":  # 종료 명령어 처리
            # 서버로 종료 명령어 전송
            client_socket.sendall(message.encode())
            # 본인 화면에 종료 메시지 출력
            print(f"나: {message}")
            break  # 메시지 입력 루프 종료
        else:
            # 서버로 입력된 메시지 전송
            client_socket.sendall(message.encode())
            # 본인 화면에 입력한 메시지를 출력
            print(f"나: {message}")
finally:
    # 프로그램 종료 시 클라이언트 소켓 닫기
    client_socket.close()
