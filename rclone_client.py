import os

import config
import subprocess
import json

config_dir = os.path.dirname(os.path.abspath(__file__))

RCLONE_BIN = '/Users/kateryna/Downloads/rclone-v1.51.0-osx-amd64/rclone'

class Rclone:
    def create_config(self, name, cloud_type, token, drive_type, drive_id):
        config_template = f"""[remote]
type = {cloud_type}
client_id = {config.CLIENT_ID}
client_secret = {config.CLIENT_SECRET}
token = {json.dumps(token)}
drive_id = {drive_id}
drive_type = {drive_type}        
        """

        file_name = f"{name}.cfg"
        with open(file_name, "w") as f:
            f.write(config_template)
        return os.path.join(config_dir, file_name)

    def copy(self, config_path, local_path, remote_path):
        command_with_args = f"{RCLONE_BIN} --config={config_path} copy remote:{remote_path} {local_path} -P"

        with subprocess.Popen(
                command_with_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True) as proc:
            (out, err) = proc.communicate()
            print(out)
            print(err)




def test():
    token = {
        "access_token": ""
    }
    name = 'my-conf'
    drive_id = "316dbd1ecb72cf5d"
    drive_type = "personal"
    cloud_type = "onedrive"

    rclone = Rclone()
    config_path = rclone.create_config(name, cloud_type, token, drive_type, drive_id)
    rclone.copy(config_path, "test_client", "backup")



test()