import os
import time
import subprocess
import configparser

def load_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file, encoding='utf-8')
        db_config = {
            "host": config.get("database", "host"),
            "port": config.getint("database", "port"),
            "user": config.get("database", "user"),
            "password": config.get("database", "password"),
            "database": config.get("database", "database"),
            "backup_dir": config.get("database", "backup_dir"),
        }
        return db_config
    except Exception as e:
        print(f"加载配置文件失败：{e}")
        return None

def backup_database(host, port, user, password, database, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)

    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    backup_file = os.path.join(backup_dir, f'{current_time}.sql')

    backup_cmd = [
        "mysqldump",
        "-h", host,
        "-P", str(port),
        "-u", user,
        f"-p{password}",
        database,
    ]

    try:
        with open(backup_file, 'w') as file:
            subprocess.run(backup_cmd, stdout=file, check=True)
        print(f"备份成功：{backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"备份失败：{e}")
        return None
    except Exception as e:
        print(f"发生意外错误：{e}")
        return None

def main():
    config_file = "config.ini"

    config = load_config(config_file)
    if not config:
        print("未能加载配置，程序退出。")
        return

    backup_database(
        config["host"],
        config["port"],
        config["user"],
        config["password"],
        config["database"],
        config["backup_dir"]
    )

if __name__ == "__main__":
    main()
