hpccm --recipe recipes/sherlock-recipe.py --format docker > Dockerfile_sherlock
docker build -t kokkos-sherlock -f Dockerfile_sherlock .
