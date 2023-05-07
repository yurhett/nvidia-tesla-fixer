import win32com.client

import os


class AddTask:
    def __init__(self):
        self.computer_name = ""
        self.computer_username = ""
        self.computer_userdomain = ""
        self.computer_password = ""
        self.action_id = "Tesla Fixer Task"
        self.action_path = r"powershell"
        self.action_arguments = r"""
            -noprofile -command "&{ start-process powershell -ArgumentList ' ((Stop-Process -Name fancontrol) -or ((Disable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *Tesla* -class Display -Status OK).InstanceId -Confirm:$false) -or (Enable-PnpDevice -InstanceId (Get-PnpDevice -FriendlyName *Tesla* -class Display -Status Error).InstanceId -Confirm:$false))) -or (Start-Process C:\Program` Files\Fan` Control\FanControl.exe)' -verb RunAs}"

                """
        self.action_workdir = r"c:\windows\system32"
        self.author = "Tesla Fixer"
        self.description = "Run Tesla Fixer when the current user logs on"
        self.task_id = self.action_id
        self.task_hidden = False
        self.username = ""
        self.password = ""

        self.TASK_TRIGGER_LOGON = 9
        self.TASK_CREATE_OR_UPDATE = 6
        self.TASK_ACTION_EXEC = 0
        self.TASK_LOGON_INTERACTIVE_TOKEN = 3

        self.scheduler = win32com.client.Dispatch("Schedule.Service")
        self.scheduler.Connect(self.computer_name or None, self.computer_username or None,
                               self.computer_userdomain or None,
                               self.computer_password or None)
        self.rootFolder = self.scheduler.GetFolder("\\")

    def add_task(self):
        taskDef = self.scheduler.NewTask(0)
        colTriggers = taskDef.Triggers

        trigger = colTriggers.Create(self.TASK_TRIGGER_LOGON)
        trigger.Id = "LogonTriggerId"
        trigger.UserId = os.environ.get('USERNAME')

        colActions = taskDef.Actions
        action = colActions.Create(self.TASK_ACTION_EXEC)
        action.ID = self.action_id
        action.Path = self.action_path
        action.WorkingDirectory = self.action_workdir
        action.Arguments = self.action_arguments

        colPrincipal = taskDef.Principal
        TASK_RUNLEVEL_HIGHEST = 1
        TASK_LOGON_SERVICE_ACCOUNT = 5
        colPrincipal.LogonType = TASK_LOGON_SERVICE_ACCOUNT
        colPrincipal.RunLevel = TASK_RUNLEVEL_HIGHEST

        info = taskDef.RegistrationInfo
        info.Author = self.author
        info.Description = self.description

        settings = taskDef.Settings
        settings.Hidden = self.task_hidden
        settings.AllowDemandStart = True
        settings.ExecutionTimeLimit = "PT0S"
        settings.StopIfGoingOnBatteries = False
        settings.DisallowStartIfOnBatteries = False

        result = self.rootFolder.RegisterTaskDefinition(
            self.task_id, taskDef, self.TASK_CREATE_OR_UPDATE, None, None, self.TASK_LOGON_INTERACTIVE_TOKEN)
        return result


if __name__ == "__main__":
    task = AddTask()
    print(task.add_task())