#!/usr/bin/env python3
import hpccm

hpccm.config.set_container_format('docker')

Stage0 += baseimage(image='ubuntu:22.04')
Stage0 += gnu()
Stage0 += cmake(eula=True)
Stage0 += openmpi(infiniband=False, cuda=False)
Stage0 += kokkos(repository="https://github.com/marcorentap/kokkos.git", branch="for-docker-braindump", cuda=False)

Stage0 += apt_get(ospackages=["net-tools", "iputils-ping", "ssh", "openssh-server"])
Stage0 += shell(commands=[
                "useradd -m -s $(which bash) marcorentap",
                "usermod -aG sudo marcorentap",
                "echo 'marcorentap:marc020630' | chpasswd"
                ])

Stage0 += copy(_chown='root',
               files={
                   '../ssh/id_rsa' : '/root/.ssh/id_rsa',
                   '../ssh/id_rsa.pub' : '/root/.ssh/id_rsa.pub',
                   '../ssh/id_rsa.pub' : '/root/.ssh/authorized_keys',
                   '../ssh/sshconfig' : '/root/.ssh/config',
})
# Stage0 += shell(commands=["cp /run/secrets/ssh_config /home/marcorentap/.ssh/config",
#                 "cp /run/secrets/id_rsa /home/marcorentap/.ssh/id_rsa",
#                 "cp /run/secrets/id_rsa_pub /home/marcorentap/.ssh/id_rsa.pub"
#                 "cp /run/secrets/id_rsa_pub /home/marcorentap/.ssh/authorized_keys"
#                 ])




Stage0 += user(user="marcorentap")
Stage0 += workdir(directory="/home/marcorentap")
# Stage0 += shell(commands=["git clone https://github.com/marcorentap/kokkos.git"])

Stage0 += shell(commands=["mkdir ~/.ssh"])
Stage0 += copy(_chown='marcorentap',
               files={
                   '../ssh/id_rsa' : '/home/marcorentap/.ssh/id_rsa',
                   '../ssh/id_rsa.pub' : '/home/marcorentap/.ssh/id_rsa.pub',
                   '../ssh/id_rsa.pub' : '/home/marcorentap/.ssh/authorized_keys',
                   '../ssh/sshconfig' : '/home/marcorentap/.ssh/config',
})

Stage0 += user(user="root")
Stage0 += shell(commands=["service ssh start"])
Stage0 += raw(docker="CMD /usr/sbin/sshd -D")
