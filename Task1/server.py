import socket  # 소켓 통신을 위한 라이브러리 임포트

# 서버 설정
HOST = '127.0.0.1'  # 서버의 IP 주소 (로컬 호스트 사용)
PORT = 5001       # 통신에 사용할 포트 번호 (임의의 번호)

# 1. 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: IPv4 주소 체계를 사용
# SOCK_STREAM: TCP 소켓을 사용

# 2. 서버 소켓에 IP 주소와 포트 바인딩
server_socket.bind((HOST, PORT))
# bind(): 소켓을 지정된 IP 주소와 포트에 연결

# 3. 클라이언트 연결 요청 대기
server_socket.listen(1)
# listen(): 소켓이 클라이언트 연결 요청을 받을 준비를 함
# (1): 최대 연결 대기 수 (여기서는 1로 설정)

print(f"서버가 {HOST}:{PORT}에서 대기 중입니다...")

# 4. 클라이언트 연결 요청 수락
conn, addr = server_socket.accept()
# accept(): 클라이언트 연결 요청을 수락하고 연결된 소켓(conn)과 주소(addr) 반환

print(f"클라이언트 {addr}와 연결되었습니다.")  # 연결된 클라이언트 주소 출력

# 클라이언트와 메시지 송수신 처리
try:
    while True:
        # 5. 클라이언트로부터 데이터 수신
        data = conn.recv(1024)
        # recv(1024): 최대 1024바이트 데이터를 수신
        # 반환된 데이터가 없으면 연결 종료

        if not data:  # 클라이언트가 연결을 종료한 경우
            break

        print(f"클라이언트: {data.decode()}")  # 수신된 메시지를 문자열로 출력

        # 6. 서버에서 클라이언트로 메시지 전송
        message = input("서버: ")  # 사용자 입력을 받아 메시지 작성
        conn.sendall(message.encode())
        # sendall(): 입력된 메시지를 바이트로 인코딩하여 전송
finally:
    # 7. 연결 종료
    conn.close()  # 클라이언트와의 연결 소켓 닫기
    server_socket.close()  # 서버 소켓 닫기
    print("서버 연결 종료")  # 종료 메시지 출력
