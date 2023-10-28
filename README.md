# lx-music-api-server
LX Music非官方测试接口服务器实现

# 开发中...

### 返回码说明
body.code：  
0: 成功  
1: IP被封禁  
2: 获取失败  
4: 服务器内部错误（对应statuscode 500）  
5: 请求过于频繁  
6: 参数错误  

statuscode:   
200: 成功  
403: IP被封禁  
400: 参数错误
429: 请求过于频繁  
500: 服务器内部错误（对应body.code 4）  