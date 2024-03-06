import requests

# 注册node_exporter服务

url = "http://10.25.10.134:8500/v1/agent/service/register"

data = {
    "id": "node-exporter-192.168.67.250",
    "name": "node-exporter-192.168.67.250",
    "address": "192.168.67.250",
    "port": 9100,
    "tags": ["firewall-develop-device"],
    "checks": [{
        "http": "http://192.168.67.250:9100/metrics",
        "interval": "5s"
    }]
}

requests.post(url, json=data)
