import socket
import threading

import cv2
import numpy as np

from server_directory import check_table
from server_directory import dbConnector


def work(conn: socket):
    company_id = None
    try:
        db = dbConnector.dbConnector('localhost', 3306, 'root', '0000', 'software_engineering');
        print("dbConnection succeeded!")

        while True:
            company_id = int((conn.recv(4)).decode())
            if db.is_id_exist(company_id):
                db.set_store_open(company_id)
            job_number = int((conn.recv(4)).decode())

            print(f"socket: c_id: {company_id}, j_num: {job_number} received")
            if job_number == 0:  # 매장 신규 생성 시그널
                new_id = db.get_last_id()
                print("새로운 아이디는 {}입니다.".format(new_id))
                conn.sendall(str(new_id).encode())
            if job_number == 1:  # 이미지 처리 시그널
                img_size = int.from_bytes(conn.recv(4), byteorder="little")
                img = conn.recv(img_size)
                encoded_img = np.fromstring(img, dtype=np.uint8)
                img = cv2.imdecode(encoded_img, cv2.IMREAD_GRAYSCALE)

                # 재용이 함수 실행
                table_pointer = db.get_table_loc_list(company_id)
                color = db.get_empty_color(company_id)
                rate = check_table.calc_rate(img, table_pointer, color)
                db.set_current_status(company_id,rate)
                # 데이터베이스 저장
                print("received")
            elif job_number == 2:  # 설정 변경 시그널
                setting = int((conn.recv(4)).decode())
                if setting == 1:
                    point_size = int((conn.recv(4)).decode())
                    point = conn.recv(point_size).decode()
                    color_size = int((conn.recv(4)).decode())
                    color = int(conn.recv(color_size).decode())

                    db.set_table_loc_list(company_id, point)
                    db.set_empty_color(company_id, color)
                    print(point, color)

                else:
                    text_size = int((conn.recv(4)).decode())
                    text = conn.recv(text_size).decode()
                    print(setting, text)
                    # 데이터베이스 매장명 변경 진행
                    if setting == 0:
                        # 매장명
                        db.set_store_name(company_id, text)
                        pass
                    elif setting == 2:
                        # 매장주소
                        db.set_store_location(company_id, text)
                        pass
                    elif setting == 3:
                        # 수용테이블
                        db.set_max_table_count_of_store(company_id, text)
                        pass

    except ValueError:
        print('input data incorrect')
        db.set_store_close(company_id)
        conn.close()
    except ConnectionError:
        print('Connection lost')
        db.set_store_close(company_id)
        conn.close()


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
