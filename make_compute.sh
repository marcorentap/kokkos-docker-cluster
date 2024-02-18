#!/bin/bash
mkdir -p ssh
rm ssh/id_rsa ssh/id_rsa.pub
ssh-keygen -f ssh/id_rsa -N ''

hpccm --recipe recipes/compute-recipe.py --format docker > Dockerfile_compute
docker build -t kokkos-compute -f Dockerfile_compute .
