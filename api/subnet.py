from ipaddress import ip_network
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/subnet', methods=['POST'])
def subnet():
    data = request.json
    ips = data.get('ips', [])  # Lista de IPs base
    hosts = data.get('hosts', [])  # Lista de hosts por red
    
    results = []
    for i, ip in enumerate(ips):
        try:
            network = ip_network(ip, strict=False)
            subnet_mask = network.subnets(new_prefix=32 - (hosts[i] - 1).bit_length())
            subnets = [{
                "network": str(sub),
                "broadcast": str(sub.broadcast_address),
                "first_host": str(sub.network_address + 1),
                "last_host": str(sub.broadcast_address - 1)
            } for sub in subnet_mask]
            results.append({"ip": ip, "subnets": subnets})
        except Exception as e:
            results.append({"ip": ip, "error": str(e)})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
