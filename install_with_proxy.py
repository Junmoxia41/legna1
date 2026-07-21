import subprocess
import sys
import os
import urllib.parse

def install_dependencies():
    print("========== INSTALADOR DE DEPENDENCIAS LEGNA v2 (PROXY MODE) ==========\n")
    
    proxy_ip = "192.105.34.1"
    proxy_port = "3128"
    
    print(f"Configuración de Proxy: {proxy_ip}:{proxy_port}")
    user = input("Usuario del Proxy: ").strip()
    password = input("Contraseña del Proxy: ").strip()

    # CODIFICACIÓN DE CREDENCIALES (Maneja el @ y otros caracteres especiales)
    user_encoded = urllib.parse.quote(user)
    pass_encoded = urllib.parse.quote(password)

    if user and password:
        proxy_url = f"http://{user_encoded}:{pass_encoded}@{proxy_ip}:{proxy_port}"
    else:
        proxy_url = f"http://{proxy_ip}:{proxy_port}"

    os.environ['HTTP_PROXY'] = proxy_url
    os.environ['HTTPS_PROXY'] = proxy_url
    
    requirements_path = "legna1/requirements.txt"
    if not os.path.exists(requirements_path):
        requirements_path = "requirements.txt"

    if not os.path.exists(requirements_path):
        print(f"Error: No se encontró {requirements_path}")
        return

    with open(requirements_path, 'r') as f:
        deps = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"\nIniciando instalación de {len(deps)} dependencias...")
    
    failed_packages = []

    for dep in deps:
        print(f"\n[Instalando] {dep}...")
        command = [
            sys.executable, "-m", "pip", "install", 
            "--proxy", proxy_url, 
            dep
        ]
        
        try:
            result = subprocess.run(command)
            if result.returncode != 0:
                print(f"⚠️  No se pudo instalar {dep}. Saltando...")
                failed_packages.append(dep)
        except Exception as e:
            print(f"❌ Error con {dep}: {e}")
            failed_packages.append(dep)

    print("\n" + "="*50)
    if not failed_packages:
        print("✅ TODAS LAS DEPENDENCIAS INSTALADAS CORRECTAMENTE.")
    else:
        print("⚠️  INSTALACIÓN FINALIZADA CON ADVERTENCIAS.")
        print(f"Los siguientes paquetes fallaron (probablemente por falta de C++ Build Tools):")
        for p in failed_packages:
            print(f"  - {p}")
        print("\nNota: Legna funcionará, pero las funciones de estos paquetes no estarán disponibles.")
    print("="*50)

if __name__ == "__main__":
    install_dependencies()
