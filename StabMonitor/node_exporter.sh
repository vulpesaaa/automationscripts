#!/bin/bash

# 下载node_exporter

curl -sL https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz -o /tmp/node_exporter.tar.gz

# 解压node_exporter

tar -xf /tmp/node_exporter.tar.gz -C /opt/netvine