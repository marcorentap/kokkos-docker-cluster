docker container rm kokkos-sherlock-$(hostname)
docker run -it --name kokkos-sherlock-$(hostname) --hostname kokkos-sherlock-$(hostname) -u compute \
--mount type=bind,source=./shared,destination=/shared \
--network kokkos-overlay kokkos-sherlock \
bash
