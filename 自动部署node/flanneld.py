#!/usr/bin/python
import sys
f=open('/etc/sysconfig/flanneld','w')
f.write('''FLANNEL_ETCD="http://%s:2379,http://%s:2379,http://%s:2379"
FLANNEL_ETCD_KEY="/kube-centos/network"
''' % (sys.argv[1],sys.argv[2],sys.argv[3]))

f.close
