import subprocess
import sys
import os
import urllib.parse

def install_dependencies():
    print("========== INSTALADOR LEGNA v3 (NUEVO MOTOR WEB-NATIVO) ==========\n")
    
    proxy_ip = "192.105.34.1"
    proxy_port = "3128"
    user = "airienrr"
    password = "5421915432k20@A"
    
    proxy_url = f"http://{urllib.parse.quote(user)}:{urllib.parse.quote(password)}@{proxy_ip}:{proxy_port}"
    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url

    command = [sys.executable, "-m", "pip", "install", "--proxy", proxy_url, "pywebview"]
    
    print("\n[Instalando] Nuevo motor de interfaz (pywebview)...")
    subprocess.run(command)
    
    print("\n✅ Instalación completa. Ya puedes ejecutar legna.py")

if __name__ == "__main__":
    install_dependencies()
