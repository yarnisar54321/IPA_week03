import paramiko

routers = [
    {"hostname": "172.31.52.1", "device": "R0"},
    {"hostname": "172.31.52.4", "device": "R1"},
    {"hostname": "172.31.52.5", "device": "R2"},
    {"hostname": "172.31.52.2", "device": "S0"},
    {"hostname": "172.31.52.3", "device": "S1"},
]

private_key_path = "C:\\Users\\Acer\\GNS3\\projects\\IPA_LAB_week3\\ppk"

for router in routers:
    try:
        key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=router["hostname"],
            username="admin",
            pkey=key
        )
        print(f" Connected to {router['device']} ({router['hostname']})")

        # ใช้คำสั่ง show running-config
        stdin, stdout, stderr = ssh.exec_command("show run")
        output = stdout.read().decode()
        print(output)

        # เซฟเฉพาะ R0 ลงไฟล์ชื่อให้ถูกต้อง
        if router["device"] == "R0":
            with open("R0_running_config.txt", "w", encoding="utf-8") as file:
                file.write(output)
            print(" Output saved to R0_running_config.txt")

        ssh.close()

    except Exception as e:
        print(f"  Failed to connect to {router['device']} ({router['hostname']}): {e}")
