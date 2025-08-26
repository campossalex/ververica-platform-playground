#!/usr/bin/env bash

# install pip and python libs
python3 ververica-platform-playground/get-pip.py
pip3 install faker kafka-python

# add a stable ubuntu repo and run ap update
rm -rf /etc/apt/sources.list
cp ververica-platform-playground/ubuntu.repo.list /etc/apt/sources.list.d/ubuntu.repo.list
apt-get update --allow-insecure-repositories

# postgresql install
apt install postgresql -y
printf '%s\n' >> "/etc/postgresql/12/main/pg_hba.conf" \
  'host     all     all     0.0.0.0/0     md5'
printf '%s\n' >> "/etc/postgresql/12/main/postgresql.conf" \
  "listen_addresses = '*'"
systemctl restart postgresql

sudo cp ververica-platform-playground/pg_ddl.sql /pg_ddl.sql
sudo chown postgres:postgres /pg_ddl.sql
sudo -i -u postgres psql -a -w -f /pg_ddl.sql

# install redpanda
curl -1sLf 'https://dl.redpanda.com/nzc4ZYQK3WRGd9sy/redpanda/cfg/setup/bash.deb.sh' | sudo -E bash && sudo apt install redpanda -y
sudo apt install redpanda -y
rm -rf /etc/redpanda/redpanda.yaml
cp ververica-platform-playground/redpanda/redpanda.yaml /etc/redpanda/redpanda.yaml
systemctl start redpanda
sudo apt-get install redpanda-console -y
printf '%s\n' >> "/etc/redpanda/redpanda-console-config.yaml" \
  'server:' \
  '  listenAddress: "0.0.0.0"' \
  '  listenPort: 9090'
systemctl start redpanda-console

#product csv to minio
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
./mc alias set vvpminio http://localhost:30004 admin password --api S3v4
./mc mb vvpminio/data
./mc mb vvpminio/data/product
./mc od if=ververica-platform-playground/data/products.csv of=vvpminio/data/product/products.csv
