#!/usr/bin/env python3
import hpccm

hpccm.config.set_container_format('docker')

Stage0 += baseimage(image='nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04')
Stage0 += gnu()
Stage0 += cmake(eula=True)
Stage0 += openmpi(infiniband=False, cuda=False)
Stage0 += kokkos(repository="https://github.com/kokkos/kokkos.git", cuda=True)

Stage0 += apt_get(ospackages=["net-tools", "iputils-ping", "ssh", "openssh-server"])
Stage0 += shell(commands=[
                "useradd -m -s $(which bash) compute",
                "usermod -aG sudo compute",
                "echo 'compute:kokkoscompute' | chpasswd"
                ])

Stage0 += copy(_chown='root',
               files={
                   '../ssh/id_rsa' : '/root/.ssh/id_rsa',
                   '../ssh/id_rsa.pub' : '/root/.ssh/id_rsa.pub',
                   '../ssh/id_rsa.pub' : '/root/.ssh/authorized_keys',
                   '../ssh/sshconfig' : '/root/.ssh/config',
})


Stage0 += user(user="compute")
Stage0 += workdir(directory="/home/compute")

Stage0 += shell(commands=["mkdir ~/.ssh"])
Stage0 += copy(_chown='compute',
               files={
                   '../ssh/id_rsa' : '/home/compute/.ssh/id_rsa',
                   '../ssh/id_rsa.pub' : '/home/compute/.ssh/id_rsa.pub',
                   '../ssh/id_rsa.pub' : '/home/compute/.ssh/authorized_keys',
                   '../ssh/sshconfig' : '/home/compute/.ssh/config',
})

Stage0 += user(user="root")
Stage0 += shell(commands=["service ssh start"])
Stage0 += raw(docker="CMD /usr/sbin/sshd -D")
