import os
from pathlib import Path

def generate_prompt(restart_paths: list, gpu_name: str) -> str:
    restart_path_prompt = ""
    restart_base_prompt = ""
    if restart_paths is not None:
        for restart_path in restart_paths:

            if " " in restart_path:
                restart_path = restart_path.replace(" ", "` ")
            restart_path_prompt = restart_path_prompt + f" -or (Start-Process {restart_path})"
            base_name = get_base_name(restart_path)
            if " " in base_name:
                base_name = base_name.replace(" ", "` ")
            restart_base_prompt = restart_base_prompt + f" (Stop-Process -Name {base_name}) -or"
    return f"""
        -noprofile -command "&{{ start-process powershell -ArgumentList ' ({restart_base_prompt} ((Disable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *{gpu_name}* -class Display -Status OK).InstanceId -Confirm:$false) -or (Enable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *Tesla* -class Display -Status Error).InstanceId -Confirm:$false))) {restart_path_prompt}' -verb RunAs}}"
"""


def get_base_name(path: str) -> str:
    filename_with_ext = os.path.basename(path)
    return str(Path(filename_with_ext).with_suffix(''))



if __name__ == '__main__':
    print(
        generate_prompt([], "Tesla"))
