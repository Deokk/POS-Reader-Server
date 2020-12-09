import socket
import threading

import cv2
import numpy as np
import ast


def work(conn: socket):
    try:
        while True:
            company_id = int((conn.recv(4)).decode())
            job_number = int((conn.recv(4)).decode())

            print(f"socket: c_id: {company_id}, j_num: {job_number} received")

            if job_number == 1:  # 이미지 처리 시그널
                img_size = int.from_bytes(conn.recv(4), byteorder="little")
                img = conn.recv(img_size)
                encoded_img = np.fromstring(img, dtype=np.uint8)
                img = cv2.imdecode(encoded_img, cv2.IMREAD_GRAYSCALE)
                # cv2.imshow('gray', img)
                # cv2.waitKey(0)
                # 만약 데이터베이스에 id가 없다면?
                # if company_id is DB 받을 부분:
                # DB에 신규 ID 생성
                #     return "생성된 company_ID는 {ID} 입니다. 매장 정보 설정을 통해 설정해주세요."
                # 재용이 함수 실행
                # rate = check_Table.calc_rate(img, table_pointer)
                # 데이터베이스 저장
                print("received")

            elif job_number == 2:  # 설정 변경 시그널
                setting = int((conn.recv(4)).decode())
                if setting == 0:
                    text_size = int((conn.recv(4)).decode())
                    text = conn.recv(text_size).decode()
                    print(text)
                    # 데이터베이스 매장명 변경 진행
                    pass
                elif setting == 1:
                    point_size = int((conn.recv(4)).decode())
                    point = ast.literal_eval(conn.recv(point_size).decode())
                    color_size = int((conn.recv(4)).decode())
                    color = ast.literal_eval(conn.recv(color_size).decode())
                    # 데이터베이스에 포지션 넣기

    except ValueError:
        print('input data incorrect')


class socket_communicator:
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, tcp_ip: str, tcp_port: int):
        self.s.bind((tcp_ip, tcp_port))
        print(f"binded {tcp_ip}, {tcp_port}")

    def run(self):
        self.listener()

    def listener(self):
        while True:
            self.s.listen(1)
            conn, addr = self.s.accept()
            print(f"connected to {addr[0]}")
            t = threading.Thread(target=work, args=(conn,))
            t.start()
