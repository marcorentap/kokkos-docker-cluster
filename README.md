# Build Images

The Dockerfiles are generated using [HPCCM](https://github.com/NVIDIA/hpc-container-maker) from recipes in `recipes/`.
The images are based on `nvcr.io/nvidia/cuda:12.3.1-devel-ubuntu22.04`;

There are two images: `kokkos-compute` and `kokkos-sherlock`. Building
`kokkos-compute` will also generate ssh keys in `ssh/` which are shared
by both images. 

You will need to specify the [architecture to build kokkos](https://kokkos.org/kokkos-core-wiki/keywords.html)
by setting the `KOKKOS_CLUSTER_ARCH` environment variable. For example, to build
the images for Kokkos_ARCH_VOLTA70, do:
```
export KOKKOS_CLUSTER_ARCH=VOLTA70
./make_compute.sh && ./make_sherlock.sh
```

Both images have the user `root` and `compute`.

# Start Containers

`kokkos-compute` containers are supposed to always be running in the background
while `kokkos-sherlock` containers can be started anytime and launch jobs.
Additionally, `shared/` is mounted to `/shared` in both images.

First build the network:
```
./make_network.sh
```

The file `compose.yaml` is configured to launch 100 `kokkos-compute` containers.
To deploy it, run:
```
docker stack deploy --compose-file=compose.yaml kokkos
```

To start a `kokkos-sherlock` container and enter bash, run:
```
./start_sherlock.sh
```

## Try something
`/shared/hostfile` is an `mpirun` hostfile with 100 hosts and 4 slot each.
`/shared/hello.sh` is a test program to print hostname. So you can run
```
mpirun --np 400 --hostfile /shared/hostfile /shared/hello.sh
```

Make sure that there are 100 compute nodes with `docker service ls` so that
all hosts listed in the hostfile actually exist.

# Scaling
In case 100 containers is not enough, and you want 150 containers, run:
```
docker service scale kokkos_compute=150
./gen_hostfile.py 4 > shared/hostfile
```

`./gen_hostfile <MPI_SLOTS>` generates a hostfile based on currently running
`kokkos-compute` containers. Make sure to check the number of running containers
with `docker service ls` before running this script.

# Stop
```
docker stack rm kokkos
```
