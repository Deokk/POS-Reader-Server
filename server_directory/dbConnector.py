import pymysql
import numpy as np
import ast
"""
design pattern :: Adapter
"""
class dbConnector:
    connector = None
    cursor = None

    def __init__(self, host: str, port: int, user: str, pwd: str, db: str):
        self.connector = pymysql.connect(
            port=port,
            user=user,
            passwd=pwd,
            host=host,
            db=db
        )
        self.cursor = self.connector.cursor(pymysql.cursors.DictCursor)  # 반환형을 tuple로

    def excute_query(self, sql: str, condition: int or str = "all") -> tuple:
        self.cursor.execute(sql)
        if condition == "all":
            return self.cursor.fetchall()
        elif condition == "one":
            return self.cursor.fetchone()
        elif type(condition) == int:
            return self.cursor.fetchmany(condition)

    def register_new_store(self,id:str, name:str, loc:str, maxSpace:int, open:int=0):
        str_for_info = "INSERT INTO store_info (storeID, storeName, storeLocation, maxSpace) VALUES ("+id+", '" + name+"', '"+loc+"', "+maxSpace+");"
        str_for_status = "INSERT INTO store_status (storeID, open, currentStatus) VALUES ("+id+", " +str(open)+", 0);"

        print(str_for_info)
        self.excute_query(str_for_info)
        print(str_for_status)
        self.excute_query(str_for_status)
        self.connector.commit()
        return True;

    def delete_store(self, id:str):
        str_for_status = "delete from store_status where storeID = "+id
        str_for_info = "delete from store_info where storeID = " + id

        self.excute_query(str_for_status)
        self.excute_query(str_for_info)
        self.connector.commit()

    def is_id_exist(self,id: str):
        target = " SELECT * FROM `store_info` where storeID = '33';"
        result = self.excute_query(target)
        if result is ():
            print("id 존재하지 않음 :: dbConnector.py line 35")
            return False
        else:
            return True

    def set_current_status(self,id:str, current_status:int):
        try:
            self.excute_query("UPDATE store_info SET maxSpace = "+str(current_status)+" where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def get_current_status(self,id:str):
        try:
            target = " SELECT currentStatus FROM store_status where storeID = "+id+";"
            answer = self.excute_query(target)
            print(type(answer))
            print(answer)
            return True
        except:
            print("오류")
            return False

    def set_store_open(self, id:str):
        try:
            self.excute_query("UPDATE store_status SET currentStatus = 1 where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def set_store_close(self, id:str):
        try:
            self.excute_query("UPDATE store_status SET open = 0 where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def get_store_open(self,id:str):
        try:
            target = " SELECT open FROM store_status where storeID = "+id+";"
            answer = self.excute_query(target)
            print(type(answer))
            print(answer)
            return True
        except:
            print("오류")
            return False

    def set_max_table_count_of_store(self,id:str, max_table_count:int):
        try:
            self.excute_query("UPDATE store_info SET maxSpace = "+str(max_table_count)+" where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def get_max_table_count_of_store(self, id:str):
        try:
            target = " SELECT maxSpace FROM store_info where storeID = "+id+";"
            answer = self.excute_query(target)
            print(type(answer))
            print(answer)
            return True
        except:
            print("오류")
            return False

    def set_store_name(self, id:str,name:str):
        try:
            self.excute_query("UPDATE store_info SET maxSpace = "+name+" where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def set_store_location(self, id:str,location:str):
        try:
            self.excute_query("UPDATE store_info SET maxSpace = "+location+" where storeID = "+id+");")
            self.connector.commit()
            return True
        except:
            return False

    def set_table_loc_list(self, id:str,array):
        array = np.asarray(array)
        if not self.array_input_valid(array):
            return False
        array = self.array_to_string(array)
        sql_command = """update store_info set tableLocList = ('"""+array+"""') where storeID="""+id+"""; """
        self.excute_query(sql_command,id)
        self.connector.commit()
        return False

    def get_table_loc_list(self, id):
        target = """ SELECT tableLocList FROM store_info where storeID = """ + id + """;"""
        response = self.excute_query(target)
        temp = response[0].get('tableLocList')
        response_as_numpy = np.array(ast.literal_eval(temp))
        print(np.shape(response_as_numpy))
        print(response_as_numpy)
        return response_as_numpy

    def array_to_string(self,array):
        target_string = "["
        if np.size(array) is np.size(array, axis=0): # 1차원 배열
            for i in range(np.size(array) - 1):
                target_string = target_string + str(array[i]) + ", "
            target_string = target_string + str(array[-1])+"]"
        else:
            for i in range(np.size(array, axis=0)):
                target_string = target_string + "["
                for j in range(np.size(array,axis=1) - 1):
                    target_string = target_string + str(array[i][j]) + ", "
                target_string = target_string + str(array[i][-1]) + "]"
                if i is not np.size(array,axis=0)-1:
                    target_string +=", "
            target_string = target_string + "]"
        print(target_string)
        return target_string

    def array_input_valid(self, array):
        # case : array가 1차원 (가게에 테이블이 하나면서 x, y가 있는 경우)
        if np.size(array, axis=0) is np.size(array):
            if np.size(array) is 4:
                return True
            else:
                print("x,y,color,bool중 누락된 것이 있거나 값이 더 들어왔습니다.")
                print("들어온 데이터의 개수 : {}".format(np.size(array)))
                return False
        else:
            if np.size(array, axis=1) is 4:
                return True
            else:
                print("x,y,color,bool 중 누락된 것이 있거나 값이 더 들어왔습니다.")
                print("들어온 데이터의 개수 : {}".format(np.size(array, axis=1)))
                return False

