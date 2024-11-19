import socket  # 소켓 통신을 위한 라이브러리 임포트

# 서버 설정
HOST = '127.0.0.1'  # 연결할 서버의 IP 주소 (로컬 호스트 사용)
PORT = 5001    # 서버와 동일한 포트 번호

# 1. 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: IPv4 주소 체계 사용
# SOCK_STREAM: TCP 소켓 사용

# 2. 서버에 연결 요청
client_socket.connect((HOST, PORT))
# connect(): 지정된 IP와 포트의 서버에 연결 요청
print(f"서버 {HOST}:{PORT}에 연결되었습니다.")  # 연결 성공 메시지 출력

# 서버와 메시지 송수신 처리
try:
    while True:
        # 3. 클라이언트에서 서버로 메시지 전송
        message = input("클라이언트: ")  # 사용자 입력을 받아 메시지 작성
        client_socket.sendall(message.encode())
        # sendall(): 입력된 메시지를 바이트로 인코딩하여 서버로 전송

        # 4. 서버로부터 데이터 수신
        data = client_socket.recv(1024)
        # recv(1024): 최대 1024바이트 데이터를 수신
        # 반환된 데이터가 없으면 연결 종료

        if not data:  # 서버가 연결을 종료한 경우
            break

        print(f"서버: {data.decode()}")  # 수신된 메시지를 문자열로 출력
finally:
    # 5. 연결 종료
    client_socket.close()  # 서버와의 연결 소켓 닫기
    print("클라이언트 연결 종료")  # 종료 메시지 출력
