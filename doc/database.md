#DataBase : law
##Table : user
* create_time:用户创建时间
* username:用户名字
* password:用户密码
* nickname:用户昵称
* rest_money:用户余额
* phone_number:手机号码
* mail:邮箱地址
* user_type:用户类型
* user_auth:是否验证用户
* 

##Table : log
* log_id:访问id
* username:访问的用户名字
* create_time:创建时间
* type:访问类型
* doc_id:访问文书的编号
* query_parameter:搜索的参数请求
* user_ip:用户的ip地址
* 

##Table : code
* code:验证码编号
* create_time:验证码创建时间
* leveltype:验证码权限等级
* 

##Table : usertype
* type_id:用户类型编号
* allow_search:是否允许搜索
* allow_view:是否允许查看文书
* allow_add:是否允许上传文书
* allow_download:是否允许下载文书
* search_perday:每天搜索次数
* search_perhour:每小时搜索次数
* view_perday:每天查看文书次数
* view_perhour:每小时查看文书次数
* 

##Table:favorite
* favorite_id:收藏夹id
* create_time:创建时间
* username:用户名字
* name:收藏夹名字
* 

##Table:favorite_item
* item_id:收藏条目id
* favorite_id:收藏夹id
* doc_id:文书id
* create_time:创建时间
* 

##Table:charge
* charge_id:充值id
* create_time:充值时间
* username:用户名字
* amount:充值金额
* type:充值方式
* 
