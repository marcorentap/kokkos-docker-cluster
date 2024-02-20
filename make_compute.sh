#!/bin/bash
hpccm --recipe recipes/compute-recipe.py --format docker > Dockerfile_compute
docker build -t kokkos-compute -f Dockerfile_compute .
