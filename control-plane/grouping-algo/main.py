import subprocess
import time
import psycopg2

time.sleep(5)

host = "192.168.50.201"
port = 30399  # SQL 포트, insecure 모드에서는 그대로 사용
database = "cluster"
user = "sysailab612"

conn = psycopg2.connect(
    dbname=database,
    user=user,
    host=host,
    port=port,
    sslmode='disable'  # insecure 모드에서는 SSL disable 필수
)
conn.autocommit = True

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"\n$ {cmd}\n{result.stdout}")
        else:
            print(f"\n$ {cmd}\nError: {result.stderr}")
    except Exception as e:
        print(f"Exception while running '{cmd}': {e}")
        
def db_insert(conn):

    with conn.cursor() as cur:
        # 테이블 생성
        # cur.execute("""
        #     CREATE TABLE IF NOT EXISTS test_table (
        #         id SERIAL PRIMARY KEY,
        #         name STRING,
        #         value INT
        #     );
        # """)

        # INSERT
        # cur.execute("INSERT INTO test_table (name, value) VALUES (%s, %s);", ('edge-node', 100))

        # SELECT
        cur.execute("SELECT * FROM hub_edge;")
        rows = cur.fetchall()
        for row in rows:
            print(f"Row: {row}")

        # UPDATE
        # cur.execute("UPDATE test_table SET value = %s WHERE name = %s;", (200, 'edge-node'))

        # DELETE
        # cur.execute("DELETE FROM test_table WHERE name = %s;", ('edge-node',))    

while True:
    run_cmd("kubectl top nodes")
    run_cmd("kubectl top pods --all-namespaces")
    run_cmd("kubectl get crd")
    run_cmd("kubectl get nodes -l node-role.kubernetes.io/hub="" -o name")
    db_insert(conn=conn)
    time.sleep(15)
    
    
    

