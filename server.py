"""One-connection TCP server for the troubleshooting lab."""

import socket


HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024


def main():
    server_socket = None
    client_socket = None

    try:
        # IPv4 TCP 소켓을 만들고, 재실행 시 같은 포트를 사용할 수 있게 한다.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        # 클라이언트 한 대의 연결을 기다린다.
        client_socket, client_address = server_socket.accept()
        print(f"[SERVER] Client connected: {client_address[0]}:{client_address[1]}")

        # 이 실습은 짧은 메시지 한 번을 주고받는다.
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            message = data.decode("utf-8")
            print(f"[SERVER] Received: {message}")

            response = f"Server received: {message}"
            client_socket.sendall(response.encode("utf-8"))
            print("[SERVER] Response sent")
        else:
            print("[SERVER] Client closed without sending data")

    except KeyboardInterrupt:
        print("\n[SERVER] Stopped by user")
    except (OSError, UnicodeDecodeError) as error:
        print(f"[ERROR] Server error: {error}")
    finally:
        # 성공하거나 오류가 나도 연결 소켓과 대기 소켓을 닫는다.
        if client_socket is not None:
            client_socket.close()
            print("[SERVER] Connection closed")
        if server_socket is not None:
            server_socket.close()


if __name__ == "__main__":
    main()
