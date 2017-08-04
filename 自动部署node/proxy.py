import socket
Hostname = socket.getfqdn(socket.gethostname())

fo=open('/etc/kubernetes/proxy','w')
fo.write('''KUBE_PROXY_ARGS="--bind-address=0.0.0.0 --hostname-override=%s --kubeconfig=/etc/kubernetes/kube-proxy.kubeconfig --cluster-cidr=10.254.0.0/16"'''% (Hostname))
fo.close
