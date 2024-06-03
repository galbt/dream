FROM docker.io/minio/minio:latest

EXPOSE 6000 6001

VOLUME ["/data"]

CMD ["minio", "server", "/buckets", "--address", ":6000", "--console-address", ":6001"]