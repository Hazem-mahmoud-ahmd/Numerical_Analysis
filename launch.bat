@echo off
cd /d "D:\.vscode\project's_stuff"
wscript //nologo "D:\.vscode\project's_stuff\launch_hidden.vbs"
start /min cmd /c "python -m http.server 8000"
timeout /t 2 >nul
start "" http://localhost:8000/project.html