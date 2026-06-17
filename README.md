# claude-code-notify
### 使用方式: 
#### Step 1
git clone本仓库，在项目目录执行下面的命令 (确保安装了pyinstaller)
```
pyinstaller -F -w --add-data "claude.ico;." claude-code-notifier.py
```

运行完毕，在 `dist` 目录下找到 `claude-code-notifier.exe` 双击运行，右下角常驻任务栏，开启Windows通知。

#### Step 2
在claude code里面让agent自己安装`SKILL.md`，skill加载完毕，后续的确认权限和任务完成均会发送到工作PC的Windows通知。
