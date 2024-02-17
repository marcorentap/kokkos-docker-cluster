docker container rm sherlock-$(hostname)
docker run -it --name sherlock-$(hostname) --hostname sherlock-$(hostname) -u compute \
--mount type=bind,source=./shared,destination=/shared \
--network kokkos-overlay kokkos-sherlock \
bash
