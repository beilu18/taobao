import pymysql
import requests
import telnetlib

conn=pymysql.connect(db="Crawler",user="root",password="123456",host="localhost",charset="utf8")
cursor=conn.cursor()

class GetIP(object):
    def delete_ip(self,ip):
        #数据库删除无效ip
        delete_sql="""
        delete from IPdaili WHERE IP='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self,ip,port):
        #判断ip是否可用
        http_url="http://www.baidu.com"
        proxy_url="http://{0}:{1}".format(ip,port)
        try:
            proxy_dic={
                "http":proxy_url,
            }
            response=requests.get(http_url,proxie=proxy_dic)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code=response.status_code
            if code>=200 and code<300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    # def telnet(self, ip,port):  # 判断是否有效
    #     try:
    #         telnetlib.Telnet(ip, port=port, timeout=3.0)
    #     except:
    #         print('connect failure')
    #         self.delete_ip(ip)
    #         return False
    #     else:
    #         print('connect success')
    #         return True

    def get_random_ip(self):
        random_sql="""
        select IP,PORT from IPdaili ORDER BY rand() limit 1
        """

        cursor.execute(random_sql)

        for ip_info in cursor.fetchall():
            ip=ip_info[0]
            port=ip_info[1]

            # judge_re = self.telnet(ip, port)
            # return self.get_random_ip()

            judge_re=self.judge_ip(ip,port)

            if judge_re:
                return "http://{0}:{1}".format(ip,port)
            else:
                return self.get_random_ip()

if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()

