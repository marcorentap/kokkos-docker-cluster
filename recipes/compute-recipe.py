#!/usr/bin/env python3
import hpccm
import os

cluster_arch = os.environ["KOKKOS_CLUSTER_ARCH"]
cuda_archs = [
    "HOPPER90",
    "ADA89",
    "AMPERE86",
    "AMPERE80",
    "TURING75",
    "VOLTA72",
    "VOLTA70",
    "PASCAL61",
    "PASCAL60",
    "MAXWELL53",
    "MAXWELL52",
    "MAXWELL50",
    "KEPLER37",
    "KEPLER35",
    "KEPLER32",
    "KEPLER30",
]

if cluster_arch in cuda_archs:
    image = 'nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04'
    # image = 'nvcr.io/nvidia/nvhpc:24.1-devel-cuda_multi-ubuntu22.04'
else:
    image = 'ubuntu:22.04'

hpccm.config.set_container_format('docker')
Stage0 += baseimage(image=image)
Stage0 += gnu()
Stage0 += cmake(eula=True)
# if cluster_arch in cuda_archs:
    # Stage0 += nvhpc(eula=True, extended_environment=True)
Stage0 += openmpi(infiniband=False, cuda=cluster_arch in cuda_archs)
Stage0 += kokkos(repository="https://github.com/kokkos/kokkos.git", arch=[cluster_arch], cuda=cluster_arch in cuda_archs)

Stage0 += apt_get(ospackages=["net-tools", "iputils-ping", "ssh", "openssh-server", "slurm", "slurmctld", "slurmd"])
Stage0 += shell(commands=[
                "useradd -m -s $(which bash) compute",
                "usermod -aG sudo compute",
                "echo 'compute:kokkoscompute' | chpasswd",
                "echo 'root:kokkosroot' | chpasswd",
                "sysctl -w kernel.perf_event_paranoid=0",
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
