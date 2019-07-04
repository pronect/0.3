from jsonrpcclient import request

ping = request("http://localhost:5000/", "ping").data.result
print(ping)
status = request("http://localhost:5000/", "status").data.result
print(status)
