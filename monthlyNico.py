import subprocess

url = input("URL: ")
title = input("Filename: ")
date = input("Date: ")
vid_id = input("Video Id: ")
fileName = f"'{date} - {title} ({vid_id}).mkv'"
content = []
print("Description: ")
# Continuously get and append multi-line user input until ctrl-d or space+enter is pressed
while True:
    try:
        inputLine = input()
    except EOFError:
        break
    if inputLine == " ":
        break
    content.append(inputLine)
# print(content)

description = ''
for line in content:
    # If the line is not a newline then append to description string
    if line != '':
        # If there is an '&' then escape it using "`&" in both python and powershell
        description = description + line
    else:
        # Appends `n`n at the end of a newline so powershell can parse as two newline
        description = description + "`n`n"
# If there is an '&' then escape it using "`&" in both python and powershell
description = description.replace('&', '"`&"')
print(description)

ffmpeg_args = ['powershell.exe', '-NoExit', 'ffmpeg', '-i', url]
ffmpeg_args += ['-user_agent', '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"']
ffmpeg_args += ['-metadata', 'date=2021', '-metadata', f'comment="{description}"', '-codec', 'copy', fileName]
try:
    process = subprocess.run(ffmpeg_args, shell=True)
    print("Return Code:", process.returncode)
except Exception as e:
    print(e)
