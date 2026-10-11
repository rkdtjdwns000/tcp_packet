"""TCP client for a normal connection or connection-refused test."""

import socket


HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 3
MESSAGE = "Network Check"
BUFFER_SIZE = 1024


def main():
    client_socket = None
    connected = False

    try:
        # IPv4 TCP 소켓에 타임아웃을 설정해 무한정 기다리지 않는다.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        print(f"[CLIENT] Connecting to {HOST}:{PORT}")
        client_socket.connect((HOST, PORT))
        connected = True
        print("[CLIENT] Connected")

        # 짧은 문자열을 바이트로 바꾸어 전송한다.
        client_socket.sendall(MESSAGE.encode("utf-8"))
        print(f"[CLIENT] Sent: {MESSAGE}")

        response = client_socket.recv(BUFFER_SIZE)
        if response:
            print(f"[CLIENT] Received: {response.decode('utf-8')}")
        else:
            print("[INFO] Server closed without a response")

    except ConnectionRefusedError:
        print("[ERROR] Connection refused")
        print(
            f"[INFO] No service may be listening on TCP port {PORT}, "
            "or a firewall may have rejected the connection."
        )
    except socket.timeout:
        print(f"[ERROR] TCP operation timed out after {TIMEOUT} seconds")
    except OSError as error:
        print(f"[ERROR] Network error: {error}")
    finally:
        if client_socket is not None:
            client_socket.close()
            if connected:
                print("[CLIENT] Connection closed")
            else:
                print("[CLIENT] Socket closed")


if __name__ == "__main__":
    main()
