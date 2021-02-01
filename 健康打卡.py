# encoding:utf-8
# -------赵甲-------2837838256@qq.com---------



import os
import re
import smtplib
import random
import requests
import time
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# session = requests.Session()


# r = session.get(login_url,headers=headers, verify=False)
# dom = etree.HTML(r.content.decode("utf-8"))

class LoginDemo():
    def __init__(self):
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            # 'Cookie': ''
        }
        self.login_url = 'https://cas.hrbeu.edu.cn/cas/login?service=http%3A%2F%2Fjkgc.hrbeu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fjkgc.hrbeu.edu.cn%252Finfoplus%252Fform%252FJSXNYQSBtest%252Fstart'
        self.logined_url = ''
        self.session = requests.Session()
        self.formData = ''

    def login(self, username, password, email):
        self.email = email
        # 访问登录页面，获取lt
        result = {}

        try:
            r = self.session.get(self.login_url, headers=self.headers, verify=False)
            dom = etree.HTML(r.content.decode("utf-8"))
            result["lt"] = dom.xpath('//input[@name="lt"]/@value')[0]
            result["execution"] = dom.xpath('//input[@name="execution"]')[0].get("value")
            # 获取JSESSIONID
            # print(r.headers)

            JSESSIONID = re.search('JSESSIONID=(.*?);', str(r.headers)).group(1)
            print(result["lt"])
        except:
            print("参数获取失败！")
            self.sendFAIL()
            return '失败'



        # get一堆东西
        # url = 'https://cas.hrbeu.edu.cn/cas/js/jquery-1.9.1.min.js;jsessionid='+JSESSIONID
        # self.session.get(url, headers=self.headers, verify=False)
        # url = 'https://cas.hrbeu.edu.cn/cas/js/jquery.cookie.js;jsessionid='+JSESSIONID
        # self.session.get(url, headers=self.headers, verify=False)
        # url = 'https://cas.hrbeu.edu.cn/cas/themes/hrbeu/style.css;jsessionid='+JSESSIONID
        # self.session.get(url, headers=self.headers, verify=False)
        # url = 'https://cas.hrbeu.edu.cn/cas/images/index_02.gif;jsessionid='+JSESSIONID
        # self.session.get(url, headers=self.headers, verify=False)
        # url = 'https://cas.hrbeu.edu.cn/cas/captcha.jpg'
        # self.session.get(url, headers=self.headers, verify=False)
        # url = 'https://cas.hrbeu.edu.cn/cas/themes/hrbeu/favicon.ico;jsessionid='+JSESSIONID
        # self.session.get(url, headers=self.headers, verify=False)

        headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Cookie': 'JSESSIONID='+JSESSIONID+'; MESSAGE_TICKET=%7B%22times%22%3A0%7D'
        }



        post_url = 'https://cas.hrbeu.edu.cn/cas/login;jsessionid='+JSESSIONID+'?service=http%3A%2F%2Fjkgc.hrbeu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fjkgc.hrbeu.edu.cn%252Finfoplus%252Fform%252FJSXNYQSBtest%252Fstart'
        post_data = {
            'username': username,
            'password': password,
            'captcha': '',
            'lt': result["lt"],
            'execution': result["execution"],
            '_eventId': 'submit',
            'submit': '登 录'
        }

        # self.headers.update(h1)
        res = self.session.post(post_url, post_data, headers=headers, verify=False)

        # print(res.headers)
        # location = re.search('Location:\s(.*?)\sContent-Length',str(res.headers)).group(1)
        # res = self.session.get(location, headers=self.headers, verify=False)

        # url1 = 'http://jkgc.hrbeu.edu.cn/infoplus/form/JSXNYQSBtest/start'
        # res = self.session.get(url1, post_data, headers=self.headers, verify=False)
        # 匹配csrfToken
        csrfToken = self.get_csrfToken()

        # 获取表格链接
        post_data1 = {
            'idc': 'JSXNYQSBtest',
            'release': '',
            'csrfToken': csrfToken,
            'formData': '{"_VAR_URL":"http://jkgc.hrbeu.edu.cn/infoplus/form/JSXNYQSBtest/start","_VAR_URL_Attr":"{}"}'
        }
        url1 = 'http://jkgc.hrbeu.edu.cn/infoplus/interface/start'
        res = self.session.post(url1, post_data1, headers=self.headers, verify=False)
        # print('--------------------------------')
        # print(res.headers)
        try:
            self.table_url = re.search('\["(.*?)"\]', str(res.text)).group(1)
        except:
            print("参数获取失败！")
            self.sendFAIL()
            return '失败'

        # 访问表格，获取stepId
        # res = self.session.get(table_url, headers=self.headers, verify=False)
        stepId = self.get_stepId()

        instanceId = self.get_instanceId(stepId, csrfToken)
        # 再post一个莫名其妙的东西，可能是
        url2 = 'http://jkgc.hrbeu.edu.cn/infoplus/interface/instance/'+str(instanceId)+'/progress'
        post_data2 = {
            'stepId': stepId,
            'csrfToken': csrfToken,
            'lang': 'zh'
        }
        # 获取时间戳
        try:
            res = self.session.post(url2, post_data2, headers={'referer': self.table_url,
                                                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},
                                    verify=False)

            timestamp = re.search('"assignTime":(.*?),',str(res.text)).group(1)
        except:
            print("参数获取失败！")
            self.sendFAIL()
            return '失败'

        time.sleep(2)
        # 上传确认还是什么？为什么会有这种东西？？？？好像没有也没问题诶，但为什么有呢？？？？
        url3 = 'http://jkgc.hrbeu.edu.cn/infoplus/interface/listNextStepsUsers'
        formData = re.sub('http://jkgc.*?/start',self.table_url, self.formData)
        formData = re.sub('"fieldYQJLjcbr".*?,|"fieldYQJLjchb".*?,|"fieldYQJLjcqtms".*?,|"fieldYQJLjcqt".*?,|"fieldYQJLjcwh".*?,|"fieldJBXXtbsf".*?,','',formData)
        formData = re.sub('"fieldCNS":false','"fieldCNS":"true"',formData)
        # formData = re.sub('"_VAR_ADDR".*?,','"_VAR_ADDR":"183.202.249.128",',formData)
        # formData = formData[:-1] + r',"groupMQJCRList": [0],"_VAR_ENTRY_NAME": "平安行动_",VAR_ENTRY_TAGS": "生活服务","fieldJBXXcsny": "","fieldCXXXjtzzs_Attr": "{\"_parent\":\"140000\"}","fieldCXXXjtzzq_Attr": "{\"_parent\":\"140600\"}","fieldSTQKglsjrq": "","fieldSTQKglsjsf": "","fieldSTQKfrsjrq": "","fieldSTQKfrsjsf": "","fieldZAshi_Attr": "{\"_parent\":\"230000\"}","fieldLHFrom": "","fieldLHTo": "","fieldCXXXdqszdstx_Attr": "{\"_parent\":\"140000\"}","fieldCXXXdqszdqtx_Attr": "{\"_parent\":\"140600\"}","fieldCXXXfxcfsj": "","fieldCXXXfxcfdhsj": "","fieldGLSJFrom": "","fieldGLSJTo": "","fieldCXXXsftjhbs1_Name": null,"fieldCXXXsftjhbs2_Attr": "{\"_parent\":\"420000\"}","fieldCXXXsftjhbq2_Attr": "{\"_parent\":\"\"}"}'
        formData = formData[:-1] + r',"groupMQJCRList": [0],"_VAR_ENTRY_NAME": "平安行动_",VAR_ENTRY_TAGS": "生活服务","fieldJBXXcsny": "","fieldSTQKglsjrq": "","fieldSTQKglsjsf": "","fieldSTQKfrsjrq": "","fieldSTQKfrsjsf": "","fieldLHFrom": "","fieldLHTo": "","fieldCXXXfxcfsj": "","fieldCXXXfxcfdhsj": "","fieldGLSJFrom": "","fieldGLSJTo": "","fieldCXXXsftjhbs1_Name": null,"fieldCXXXsftjhbq2_Attr": "{\"_parent\":\"\"}"}'
        formData = re.sub(' ','',formData)
        # formData = formData.encode('utf-8')
        boundFields = 'fieldCXXXdqszdjtx,fieldCXXXjtgjbc,fieldGLJL,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldGLFS,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldFHJH,fieldJBXXjjlxrdh,fieldJBXXxm,fieldZXZT,fieldCXXXsftjhbq2,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldHGCZDM,fieldCXXXssh,fieldLHTJSX,fieldCXXXfxcfdhsj,fieldZAsheng,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldLHFrom,fieldHelp,fieldFLid,fieldYQJLjrsfczbl,fieldGLSJTo,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldZAjtwz,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldCXXXdqszdshengtx,fieldSTQKgm,fieldCXXXjtzzq,fieldLHJH,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXdqszdqtx,fieldCXXXdqszdstx,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldCXXXsftjhbs2,fieldSTQKsfstbs,fieldCXXXsftjhbs1,fieldCXXXcqwdq,fieldGLSJFrom,fieldCXXXjtfszj,fieldSFLB,fieldZAqu,fieldZAZT,fieldCXXXjtzz,fieldLHTo,fieldCXXXjtfsqt,fieldSTQKfrsjsf,fieldZAshi,fieldHGCSULY,fieldSTQKglsjsf,fieldJBXXdw,fieldCFDD,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs'

        post_data3 = {
            'actionId': '1',
            'boundFields': boundFields,
            'csrfToken': csrfToken,
            'formData': formData,
            'lang': 'zh',
            'rand': str(random.random() * 999),
            'stepId': stepId,
            'timestamp': timestamp
        }
        res = self.session.post(url3, post_data3, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'referer': self.table_url,'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest'}, verify=False)

        time.sleep(2)
        # 最终上传
        url4 = 'http://jkgc.hrbeu.edu.cn/infoplus/interface/doAction'
        post_data4 = {
            'actionId': '1',
            'boundFields': 'fieldCXXXdqszdjtx,fieldCXXXjtgjbc,fieldGLJL,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldGLFS,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldFHJH,fieldJBXXjjlxrdh,fieldJBXXxm,fieldZXZT,fieldCXXXsftjhbq2,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldHGCZDM,fieldCXXXssh,fieldLHTJSX,fieldCXXXfxcfdhsj,fieldZAsheng,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldLHFrom,fieldHelp,fieldFLid,fieldYQJLjrsfczbl,fieldGLSJTo,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldZAjtwz,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldCXXXdqszdshengtx,fieldSTQKgm,fieldCXXXjtzzq,fieldLHJH,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXdqszdqtx,fieldCXXXdqszdstx,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldCXXXsftjhbs2,fieldSTQKsfstbs,fieldCXXXsftjhbs1,fieldCXXXcqwdq,fieldGLSJFrom,fieldCXXXjtfszj,fieldSFLB,fieldZAqu,fieldZAZT,fieldCXXXjtzz,fieldLHTo,fieldCXXXjtfsqt,fieldSTQKfrsjsf,fieldZAshi,fieldHGCSULY,fieldSTQKglsjsf,fieldJBXXdw,fieldCFDD,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs',
            'csrfToken': csrfToken,
            'formData': formData,
            'lang': 'zh',
            'nextUsers': '{}',
            'rand': str(random.random() * 999),
            'remark': '',
            'stepId': stepId,
            'timestamp': timestamp
        }
        res = self.session.post(url4, post_data4, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36', 'referer': self.table_url,'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest'}, verify=False)
        print(res.text)
        print('\n--------------------------------------------------------\n')
        print(formData)
        print(self.table_url)

        result = re.search('\"ecode\":\"(.*?)\",\"entities',str(res.text)).group(1)

        if result == 'SUCCEED':
            print('成功')
            # 发邮件通知
            self.sendSUCCEED()
            return '成功'
        else:
            print('失败')
            self.sendFAIL()

            return '失败'


    # def get_lt(self):
    #     result = {}
    #
    #     r = self.session.get(self.login_url, verify=False)
    #     dom = etree.HTML(r.content.decode("utf-8"))
    #
    #     try:
    #         result["lt"] = dom.xpath('//input[@name="lt"]/@value')[0]
    #         result["execution"] = dom.xpath('//input[@name="execution"]')[0].get("value")
    #         print(result["lt"])
    #     except:
    #         print("lt参数获取失败！")
    #
    # def get_JSESSIONID(self):
    #     JSESSIONID = re.search('JSESSIONID=(.*?);',self.rr).group(1)

    def get_csrfToken(self):
        url1 = 'http://jkgc.hrbeu.edu.cn/infoplus/form/JSXNYQSBtest/start'

        try:
            r = self.session.get(url1, headers=self.headers, verify=False)
            dom = etree.HTML(r.content.decode("utf-8"))

            csrfToken = dom.xpath('//meta[@itemscope="csrfToken"]/@content')[0]
            print(csrfToken)
            return csrfToken
        except:
            print("参数获取失败！")
            self.sendFAIL()

    def get_stepId(self):
        # 获取stepId
        url1 = self.table_url

        try:
            r = self.session.get(url1, headers=self.headers, verify=False)
            # dom = etree.HTML(r.content.decode("utf-8"))

            stepId = re.search('formStepId\s=\s(.*?);',str(r.text)).group(1)
            print(stepId)
            return stepId
        except:
            print("参数获取失败！")
            self.sendFAIL()

    def get_instanceId(self, stepId, csrfToken):


        url2 = 'http://jkgc.hrbeu.edu.cn/infoplus/interface/render'
        post_data2 = {
            'stepId': stepId,
            'instanceId': '',
            'admin': 'false',
            'rand': str(random.random() * 999),
            'width': '1280',
            'lang': 'zh',
            'csrfToken': csrfToken
        }
        try:

            r = self.session.post(url2, post_data2, headers={'referer': self.table_url,
                                                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},
                                  verify=False)
            self.formData = re.search('"data":(.*?),"snapshots"', str(r.text)).group(1)
            instanceId = re.search('"instanceId":"(.*?)"', str(r.text)).group(1)
            print(instanceId)
            return instanceId
        except:
            print("参数获取失败！")
            self.sendFAIL()

    def sendSUCCEED(self):
        os.system('echo "打卡成功" | mail -s "打卡成功" ' + self.email)

    def sendFAIL(self):
        # 发送邮件
        if i == 1:
            os.system('echo "打卡失败" | mail -s "打卡失败%d,手动打卡吧"'%i + self.email)
        else:
            os.system('echo "打卡失败" | mail -s "打卡失败%d"'%i + self.email)



if __name__ == "__main__":

    status = '失败'
    i = 5
    while (status == '失败') & (i>0):
        logindemo = LoginDemo()
        status = logindemo.login(学号, '密码', '个人邮箱')
        i = i-1
    # logindemo.get_stepId()
