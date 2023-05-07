# nvidia-tesla-fixer
## 解释
很多在Windows上使用Nvidia Tesla和AMD独立显卡实现双显卡的用户可能会在Windows 11 22H2上遇到重启后无法正常调用Tesla显卡的问题，重启显卡即可恢复。
## 原理
在Windows任务计划程序处设置一个启动时执行的脚本，每次启动Windows就重启显卡，同时重启依赖NVAPI的程序。
## 使用方法
### 1. 从release下载并解压
### 2. 编辑 config.yaml
```yaml
gpu: Tesla
restart:
- C:\Program Files\Fan Control\FanControl.exe
# 每个”-“后面写依赖NVAPI的程序的路径，一行一个，注意缩进，如果没有，则请只删除内容而不删除”-“
```
### 3. 以管理员身份运行 main.exe
### 4. 重启电脑