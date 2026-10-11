"""Probe a configurable destination to compare refusal with timeout."""

import socket


# 실습 환경에 맞게 바꾼다. 이 IP에서 반드시 타임아웃이 나지는 않는다.
HOST = "192.168.100.250"
PORT = 5000
TIMEOUT = 3

# Connection Refused: 호스트에 도달했더라도 포트에 리스너가 없거나 연결이
# 거부될 수 있다. SYN 뒤에 RST 응답이 보이는 경우가 많다.
# Connection Timeout: SYN에 응답이 없을 수 있다. Firewall Drop, 라우팅 문제,
# Host Down, 네트워크 단절 등 여러 원인이 가능하다.


def main():
    client_socket = None
    connected = False

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        print(f"[TIMEOUT TEST] Connecting to {HOST}:{PORT}")
        client_socket.connect((HOST, PORT))
        connected = True
        print("[INFO] Connected; this destination did not reproduce a timeout")

    except ConnectionRefusedError:
        print("[ERROR] Connection refused")
        print(f"[INFO] TCP port {PORT} may have no listener or was rejected")
    except socket.timeout:
        print("[ERROR] Connection timeout")
        print(f"[INFO] No TCP response was received within {TIMEOUT} seconds.")
    except OSError as error:
        print(f"[ERROR] Network/OS error: {error}")
        print("[INFO] Check the address, route, and local network conditions")
    finally:
        if client_socket is not None:
            client_socket.close()
            if connected:
                print("[TIMEOUT TEST] Connection closed")
            else:
                print("[TIMEOUT TEST] Socket closed")


if __name__ == "__main__":
    main()
