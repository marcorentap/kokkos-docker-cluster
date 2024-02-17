#!/usr/bin/python3
import sys
import os
import subprocess
import json

if (len(sys.argv) < 2):
    print("Usage: ./gen_hostfile.py <MPI_SLOTS>")
    print("e.g. ./gen_hostfile.py 1 > shared/hostfile")
    exit(-1)

slots = int(sys.argv[1])
ps = subprocess.getoutput("docker service ps --format '{{json .}}' kokkos_compute")
for p in ps.split('\n'):
    j = json.loads(p)
    if (j['DesiredState'] == 'Running'):
        id = j['Name'].split(".")[1]
        print(f"kokkos-compute-{id} slots={slots}")

