#!/usr/bin/python
import os,sys,socket
Hostname = socket.getfqdn(socket.gethostname())
Localip = socket.gethostbyname(Hostname)

fo=open('/etc/kubernetes/kubelet','w')
fo.write('''KUBELET_ADDRESS="--address=%s"
KUBELET_HOSTNAME="--hostname-override=%s"
KUBELET_API_SERVER="--api-servers=http://%s:8080"
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/architect/pod-infrastructure:latest"
KUBELET_ARGS="--cgroup-driver=systemd --cluster-dns=10.254.0.2 --experimental-bootstrap-kubeconfig=/etc/kubernetes/bootstrap.kubeconfig --kubeconfig=/etc/kubernetes/kubelet.kubeconfig --require-kubeconfig --cert-dir=/etc/kubernetes/ssl --cluster-domain=cluster.local. --hairpin-mode promiscuous-bridge --serialize-image-pulls=false"''' %(Localip,Hostname,sys.argv[1]))
fo.close
