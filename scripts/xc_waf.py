import requests
import os
import json
import sys

XC_API_TOKEN = os.getenv("XC_API_TOKEN")

if not XC_API_TOKEN:
    print("❌ Missing XC_API_TOKEN")
    sys.exit(1)

BASE_URL = "https://f5latam.console.ves.volterra.io"
NAMESPACE = "m-ocampo"
LB_NAME = "demo-multicloud-mao"

HEADERS = {
    "Authorization": f"APIToken {XC_API_TOKEN}",
    "Content-Type": "application/json"
}

# 1. Leer policy
with open("security/waf/waf-policy.json") as f:
    waf_policy = json.load(f)

policy_name = waf_policy["metadata"]["name"]

print(f"📄 Applying WAF policy: {policy_name}")

# 2. Crear/actualizar policy
policy_url = f"{BASE_URL}/api/config/namespaces/{NAMESPACE}/app_firewalls"

resp = requests.post(policy_url, headers=HEADERS, json=waf_policy)

# Si ya existe, ignoramos error 409
if resp.status_code not in [200, 201, 409]:
    print("❌ Error creating WAF policy")
    print(resp.status_code, resp.text)
    sys.exit(1)

if resp.status_code == 409:
    print("ℹ️ WAF policy already exists, continuing...")

else:
    print("✅ WAF policy created/updated")

# 3. Obtener Load Balancer
lb_url = f"{BASE_URL}/api/config/namespaces/{NAMESPACE}/http_loadbalancers/{LB_NAME}"

lb_resp = requests.get(lb_url, headers=HEADERS)

if lb_resp.status_code != 200:
    print("❌ Error getting Load Balancer")
    print(lb_resp.status_code, lb_resp.text)
    sys.exit(1)

lb_data = lb_resp.json()

# 4. Validar estructura
if "spec" not in lb_data:
    print("❌ LB spec not found")
    sys.exit(1)

# 🔥 5. FIX CRÍTICO: eliminar disable_waf si existe
if "disable_waf" in lb_data["spec"]:
    print("🧹 Removing disable_waf to avoid conflict...")
    del lb_data["spec"]["disable_waf"]

# 6. Configurar WAF
lb_data["spec"]["app_firewall"] = {
    "name": policy_name,
    "namespace": NAMESPACE
}

lb_data["spec"]["enable_app_firewall"] = True

print("🔐 Attaching WAF to Load Balancer...")

# 7. Actualizar LB
update_resp = requests.put(lb_url, headers=HEADERS, json=lb_data)

if update_resp.status_code != 200:
    print("❌ Error updating Load Balancer")
    print(update_resp.status_code, update_resp.text)
    sys.exit(1)

print("🚀 WAF successfully enabled on Load Balancer!")