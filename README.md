# Requirements
- [HPCCM](https://github.com/NVIDIA/hpc-container-maker)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html)

Then change `/etc/docker/daemon.json` to use nvidia runtime by default
```
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "/usr/bin/nvidia-container-runtime"
        }
    },
    "default-runtime" :  "nvidia",
}
```

Restart docker
```
sudo systemctl restart docker
```

Make sure you have access to the GPU with the default runtime
```
docker run -it nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04 nvidia-smi
```

---

# Build Images

The Dockerfiles are generated using HPCCM from recipes in `recipes/`.
The images are based on `nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04`;

There are two images: `kokkos-compute` and `kokkos-sherlock`. Building
`kokkos-compute` will also generate ssh keys in `ssh/` which are shared
by both images. 

You will need to specify the [architecture to build kokkos](https://kokkos.org/kokkos-core-wiki/keywords.html#keywords-arch)
by setting the environment variable `KOKKOS_CLUSTER_ARCH=<TARGET_ARCH>`. The scripts will pass `Kokkos_ARCH_<TARGET_ARCH>`
compile flag to build Kokkos. For example, to build the images for Kokkos_ARCH_VOLTA70, do:
```
export KOKKOS_CLUSTER_ARCH=VOLTA70
./make_compute.sh && ./make_sherlock.sh
```

Both images have the user `root` and `compute`.

# Start Containers

`kokkos-compute` containers are supposed to always be running in the background
while `kokkos-sherlock` containers can be started anytime and launch jobs.
Additionally, `shared/` is mounted to `/shared` in both images.

First build the `kokkos-overlay` network:
```
./make_network.sh
```

The file `compose.yaml` is configured to launch 100 `kokkos-compute` containers.
To deploy it, run:
```
# if you're not already part of a swarm...
docker swarm init
docker stack deploy --compose-file=compose.yaml kokkos
```
First make sure that all 100 containers has started with
`docker service ls`. Then, start a `kokkos-sherlock` container with:
```
./start_sherlock.sh
```

## Try something
`/shared/hostfile` is an `mpirun` hostfile with 100 hosts and 4 slot each.
`/shared/hello.sh` is a test program to print hostname:
```
mpirun --np 400 --hostfile /shared/hostfile /shared/hello.sh
```

# Scaling
In case 100 containers is not enough, and you want 150 containers, run:
```
docker service scale kokkos_compute=150
./gen_hostfile.py 4 > shared/hostfile
```

`./gen_hostfile <MPI_SLOTS>` generates a hostfile based on currently running
`kokkos-compute` containers.

# Stop
```
docker stack rm kokkos
```
