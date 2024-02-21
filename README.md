# Prerequisites
Ensure you have the following tools installed:
- [HPCCM](https://github.com/NVIDIA/hpc-container-maker)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)

Modify `/etc/docker/daemon.json` to set the NVIDIA runtime as the default:
```
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "/usr/bin/nvidia-container-runtime"
        }
    },
    "default-runtime" :  "nvidia"
}
```
Then restart Docker:
```
sudo systemctl restart docker
```

Ensure GPU access with the default runtime:
```
docker run -it nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04 nvidia-smi
```

---
# Usage

## Building Images

Dockerfiles are generated using HPCCM from recipes located in `recipes/`. These images are based on `nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04`.

There are two images: `kokkos-compute` and `kokkos-sherlock`, both sharing SSH keys found in `ssh/`. To specify the architecture for building `kokkos`, set the environment variable `KOKKOS_CLUSTER_ARCH=<TARGET_ARCH>`. The scripts will then use the `Kokkos_ARCH_<TARGET_ARCH>` compile flag for building `Kokkos`. For example, to generate SSH keys and build the images for `Kokkos_ARCH_VOLTA70`, execute:
```
export KOKKOS_CLUSTER_ARCH=VOLTA70
./make_keys && ./make_compute.sh && ./make_sherlock.sh
```

Both images contain users `root` with password `kokkosroot` and `compute` with password `kokkoscompute`.

## Starting Containers

`kokkos-compute` containers are intended to run continuously in the background, while `kokkos-sherlock` containers can be started as needed to launch jobs. Additionally, `shared/` is mounted to `/shared` in both images.

Start by building the `kokkos-overlay` network:
```
# Initialize Docker swarm if not already done
docker swarm init
./make_network.sh
```

The file `compose.yaml` is configured to launch 100 `kokkos-compute` containers. To deploy it, run:
```
docker stack deploy --compose-file=compose.yaml kokkos
```
Ensure that all 100 containers have started with `docker service ls`. Then, start a `kokkos-sherlock` container using:
```
./start_sherlock.sh
```

## Try mpirun
`/shared/hostfile` contains an `mpirun` hostfile with 100 hosts and 4 slots each.
`/shared/hello.sh` is a test program to print hostnames:
```
mpirun --np 400 --hostfile /shared/hostfile /shared/hello.sh
```

## Scaling
If 100 containers are insufficient and you require 150 containers, execute:
```
docker service scale kokkos_compute=150
./gen_hostfile.py 4 > shared/hostfile
```
`./gen_hostfile <MPI_SLOTS>` generates a hostfile based on currently running `kokkos-compute` containers.

## Stopping
To stop the setup, execute:
```
docker stack rm kokkos
```
