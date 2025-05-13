import subprocess
import time

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"\n$ {cmd}\n{result.stdout}")
        else:
            print(f"\n$ {cmd}\nError: {result.stderr}")
    except Exception as e:
        print(f"Exception while running '{cmd}': {e}")

while True:
    run_cmd("kubectl top nodes")
    run_cmd("kubectl top pods --all-namespaces")
    run_cmd("kubectl get crd")
    run_cmd("kubectl get nodes -l node-role.kubernetes.io/hub="" -o name")
    time.sleep(10)
