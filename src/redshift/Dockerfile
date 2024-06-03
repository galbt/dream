FROM postgres:latest

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Expose the PostgreSQL port
EXPOSE 5432

# Start PostgreSQL service
CMD ["postgres", "-D", "/var/lib/postgresql/data"]