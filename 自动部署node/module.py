#!/usr/bin/env python
#coding=utf-8
#运行方式: fab -f module.py kernel or flannel


import os,sys
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

#下方是远程服务器的信息
env.port='22'
env.user='root'
env.hosts=['10.15.184.53','10.15.184.54']
env.password='1q2w3e4r'

#下列是etcd地址
etcd1='10.15.184.50'
etcd2='10.15.184.51'
etcd3='10.15.184.52'
#下列是master的地址
Masterapi='10.15.184.50'

@task
def kernel():
  with cd('/tmp/'):
    with settings(hide('warnings'),warn_only=True):
      url='https://www.elrepo.org'
      run('rpm --import %s/RPM-GPG-KEY-elrepo.org' % (url)).failed
      run('rpm -Uvh %s/elrepo-release-7.0-2.el7.elrepo.noarch.rpm' % (url)).failed
      run('yum --enablerepo=elrepo-kernel install -y kernel-lt-devel kernel-lt').failed
      run('grub2-set-default 0 && systemctl disable firewalld').failed

@task
def flannel():
  with cd('/tmp/'):
    with settings(hide('warnings'),warn_only=True):
      result=run('yum install -y flannel && systemctl enable flanneld')
      result.failed
      put('flanneld.py','/tmp/',mode=755)
      run('python /tmp/flanneld.py %s %s %s' %(etcd1,etcd2,etcd3))

@task
def docker():
  with cd('/tmp/'):
    with settings(hide('warnings'),warn_only=True):
      result=run('yum install docker -y && systemctl enable docker')
      result.failed
      put('daemon.json','/etc/docker/daemon.json')


@task
def k8_node():
  with cd('/tmp/'):
    with settings(hide('warnings'),warn_only=True):
      run('mkdir /var/lib/kubelet')
      PathList=['/etc/kubernetes/ssl','/root/.kube']
      for Kpath in PathList:
        run ('mkdir -p %s' % Kpath)

      try:
        put('k8s/bin/*','/usr/local/bin/',mode=755)
        put('k8s/config/*','/etc/kubernetes/',mode=644)
        put('k8s/service/*','/etc/systemd/system/')
        put('/root/.kube/config","/root/.kube/')
      except Exception, e:
        print e

      put('./config.py','/tmp/',mode=755)
      put('./proxy.py','/tmp/',mode=755)
      put('./kubelet.py','/tmp/',mode=755)
      run('python /tmp/config.py %s' % (Masterapi))
      run('python /tmp/kubelet.py %s' % (Masterapi))
      run('python /tmp/proxy.py')
      servicelist=['kube-controller-manager.service','kubelet.service','kube-proxy.service','kube-scheduler.service']
      for i in servicelist:
        run('systemctl enable %s' % i)

@task
def main():
  kernel()
  flannel()
  docker()
  k8_node()
