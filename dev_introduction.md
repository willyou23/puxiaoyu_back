# Process

## frontend

创建vue project

vue version:@vue/cli 4.5.12

```
vue create puxiaoyu_frontend
manually
babel+router+2.x
no
package.json
no
```

```
npm run serve
```

安装element-ui

```
npm i element-ui -S
```

完整引入elemet-ui    ---------在main.js

```
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
```

安装axios

```
npm install axios --save
```

引入axios

```
import axios from "axios";
Vue.prototype.$axios = axios
```

设置跨域

加入vue.config.js

安装qs

```
npm install qs
```



## backend

pycharm：创建django project

在里面创建app文件夹

```
python manage.py startapp app
```

复制model和setting，仔细比对

实现跨域

```
pip install django-cors-headers
```

安装pillow，ImageField才可以运行

```
pip install pillow
```

安装mysql包

确保migrations内没有多余文件，除了\_\_init\_\_.py

连接数据库

运行下两条语句

```
python manage.py makemigrations
python manage.py migrate
```





## Git

```
git clone https:***
//copy-paste
cd filename
git add .
git commit -m ""
git push -u origin main
```

