# “微信抢票应用”测试报告

魏宇轩 软硕192 2019214497

## 测试内容

- 单元测试
- 功能测试
- 性能测试

## 实验平台

- Ubuntu 16.0.4
- Python 3.7.0
- Django 1.9.13

- Django Server

## code review

### $PROJECT_ROOT

| Folder/File       | Description                         |
| ----------------- | ----------------------------------- |
| **adminpage/**    | 后台管理Application                 |
| **codex/**        | 自定义视图和异常类                  |
| **static/**       | 静态网页资源（html/css/javascript） |
| **templates/**    | 网页模板                            |
| **userpage/**     | 活动票务展现Application             |
| **wechat/**       | 微信抢票Application                 |
| **WeChatTicket/** | 项目主Application                   |
| configs.json      | setting配置文件                     |
| manage.py         | Django项目入口                      |
| requirements.txt  | 项目安装依赖文件                    |

### WeChatTicket/
项目主入口App，由Django框架自动生成，修改`urls.py`配置路由  

| File            | Description  |
| --------------- | ------------ |
| \_\_init\_\_.py | Python包文件 |
| settings.py     | 配置文件     |
| urls.py         | 路由         |
| views.py        | 视图         |
| wsgi.py         | WSGI服务器入口 |

### wechat/
微信抢票App，定义了用户、活动、票务的数据模型，基于微信接口开发了抢票相关功能  

| File            | Description  |
| --------------- | ------------ |
| **management/**     | 自定义微信相关Django command命令目录     |
| **migrations/**     | 数据库迁移文件目录（自动生成）     |
| \_\_init\_\_.py | Python包文件 |
| admin.py     | 后台注册     |
| apps.py     | App配置     |
| handlers.py     | 微信功能接口     |
| models.py         | 数据库对象模型 |
| settings.py     | 配置文件     |
| views.py        | 视图         |
| wrapper.py         | 微信接口底层封装         |

### userpage/
活动票务展现App  

| File            | Description  |
| --------------- | ------------ |
| \_\_init\_\_.py | Python包文件 |
| admin.py     | 后台注册     |
| apps.py     | App配置     |
| models.py         | 空 |
| urls.py     | 路由     |
| views.py        | 视图         |

### userpage/
后台管理App  

| File            | Description  |
| --------------- | ------------ |
| \_\_init\_\_.py | Python包文件 |
| admin.py     | 后台注册     |
| apps.py     | App配置     |
| decorator.py     | 装饰器     |
| models.py         | 空 |
| urls.py     | 路由     |
| views.py        | 视图         |

## 生成测试数据
### 数据库配置
| 库名 | wechat_ticket |
| --------------- | ------------ |
| username  |   root    |
| password  |   o443W586A2  |
| ip    | 127.0.0.1 |
| port  | 3306  |
### 生成数据表
利用Django框架自动按照`./wecaht/models.py`生成数据表`wechat_activity`, `wechat_ticket `, `wechat_user`
```sql
mysql> show tables;
+----------------------------+
| Tables_in_wechat_ticket    |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| wechat_activity            |
| wechat_ticket              |
| wechat_user                |
+----------------------------+
13 rows in set (0.00 sec)
```
### 生成测试数据
- 用`python manager.py createsuperuser`命令创建管理员超级用户  
    - username: root
    - password: ！root123
- 使用Python脚本向MySQL插入测试用户数据
```python
"""
insert test data into database for unit test and function test
"""

import MySQLdb


db = MySQLdb.connect('127.0.0.1', 'root', 'o443W586A2', 'wechat_ticket')

cursor = db.cursor()

sql = """INSERT INTO wechat_user(open_id, to_active) VALUES ('weiyx', 1)"""

try:
    cursor.execute(sql)
    db.commit()
    print('success~~')
except:
    db.rollback()
    print('fail~~')

db.close()

```
```sql
mysql> select * from wechat_user;
+----+---------+-----------+----------------+
| id | open_id | to_active | system_user_id |
+----+---------+-----------+----------------+
|  5 | weiyx   |         1 |           NULL |
+----+---------+-----------+----------------+
1 row in set (0.00 sec)

```

## 单元测试
### 测试范围
`adminpage/views.py`中的各个类  
![test_classes](md_imgs/test_classes.png)
### 管理员登录

### 管理员登出

### 活动列表

### 创建活动

### 删除活动

### 抢票菜单

### 图片上传

### 检票


## 功能测试
### 测试范围
```python
urlpatterns = [
    url(r'^login/?$', AdminLoginView.as_view()),
    url(r'^logout/?$', AdminLogoutView.as_view()),
    url(r'^activity/list/?$', ActivityList.as_view()),
    url(r'^activity/detail/?$', ActivityDetail.as_view()),
    url(r'^activity/create/?$', ActivityCreate.as_view()),
    url(r'^activity/delete/?$', ActivityDelete.as_view()),
    url(r'^activity/menu/?$', ActivityMenu.as_view()),
    url(r'^image/upload/?$', ImageUpload.as_view()),
    url(r'^activity/checkin/?$', ActivityCheckin.as_view())
]
```
### 管理员登录
#### 测试用例
1. 正确用户名 + 正确密码
2. 错误用户名
3. 正确用户名 + 错误密码
#### 测试代码
```python
class AdminLoginViewTest(FunctionTestWrapper):
    def test_valid_login(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('root')

        inputPassword.clear()
        inputPassword.send_keys('!root123')

        loginnow.click()
        time.sleep(2)

        self.assertEqual(self.browser.title, '活动列表 - 紫荆之声')     # check if jump to activity list page

        cookies = self.browser.get_cookies()

        with open('admin_cookies.json', 'w') as f:
            json.dump(cookies, f)

    def test_invalid_username(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('weiyx')

        inputPassword.clear()
        inputPassword.send_keys('!root123')

        loginnow.click()

        self.assertEqual(self.browser.find_element_by_id('alert').text, '用户名或密码错误')

    def test_wrong_password(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('root')

        inputPassword.clear()
        inputPassword.send_keys('root')

        loginnow.click()

        self.assertEqual(self.browser.find_element_by_id('alert').text, '用户名或密码错误')
```
#### 测试结果
![AdminLoginViewTest](md_imgs/AdminLoginTest.png)

### 管理员登出

### 活动列表

### 创建活动

### 删除活动

### 抢票菜单

### 图片上传

### 检票



