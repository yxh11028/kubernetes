脚本主程序是module.py
```
运行方式是fab -f module.py main
```
如果想单装其中一个组件。使用
```
fab -f module.py kernel
```
可选方式
```
kernel
flannel
docker
k8_node
```

脚本可远程批量安装node。 随手写的，功能比较简单。
