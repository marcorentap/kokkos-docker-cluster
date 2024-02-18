#!/bin/bash
docker network rm kokkos-overlay
docker network create --driver overlay --subnet=192.168.64.0/18 --attachable  kokkos-overlay
