import os

import yaml
from utils.win32task import AddTask
from utils.powershell import generate_prompt

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        data = yaml.safe_load(f)
    task = AddTask()
    prompt = generate_prompt(data['restart'], data['gpu'])
    task.action_arguments = prompt
    task.add_task()
    print("Success")
    os.system("pause")

"""
-noprofile -command "&{ start-process powershell -ArgumentList ' ( (Stop-Process -Name FanControl.exe)  -or ((Disable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *Tesla* -class Display -Status OK).InstanceId -Confirm:$false) -or (Enable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *Tesla* -class Display -Status Error).InstanceId -Confirm:$false)))  -or (Start-Process C:\Program` Files\Fan` Control\FanControl.exe)' -verb RunAs}"
"""