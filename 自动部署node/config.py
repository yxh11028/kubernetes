#!/usr/bin/python
import socket,os,sys

fo=open('/etc/kubernetes/config','w')
fo.write('''KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=true"
KUBE_MASTER="--master=http://%s:8080"
''' %(sys.argv[1]))
fo.close


