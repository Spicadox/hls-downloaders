import subprocess
import re


# the m3u8 url
url = input("URL: ")
title = input("Filename: ")
artist = input("Artist: ")
# e.g. 2021-10-12 or 20211012
date = input("Date: ")

# forbidden character replacement
# fixed_name = orig_name.replace('\\\\','⑊')
# forbidden_characters = '"*/:<>?\|'
# unicode_characters = '”⁎∕꞉‹›︖＼⏐'
# for a, b in zip(forbidden_characters, unicode_characters):
#     fixed_name = fixed_name.replace(a, b)


# Replace double quotes with “ which is a Unicode character U+201C “, the LEFT DOUBLE QUOTATION MARK. Note: ” U+201D is a Right Double Quotation Mark
# Replace < and > with unicode fullwidth less-than sign and fullwidth less-than sign
# Replace : with unicode character U+A789 ꞉ which is a Modifier Letter Colon
# Replace / with unicode character U+2215 ⁄ which is a unicode division slash
# Replace ? with unicode character U+FF1F ？ which is a fullwidth question mark
# Replace \ with unicode character U+29F5 ⧵ which is a Reverse Solidus Operator
# Replace * with unicode character U+204E ⁎ which is a Low Asterisk
# Replace | with unicode character U+23D0 ⏐ which is a Vertical Line Extension
title = title.replace('"', '“').replace("<", "＜").replace(">", "＞").replace(":", "꞉").replace("/", "∕").replace("?", "？").replace("\\", "⧵").replace("*", "⁎").replace("|", "⏐")
artist = artist.replace('"', '“').replace("<", "＜").replace(">", "＞").replace(":", "꞉").replace("/", "∕").replace("?", "？").replace("\\", "⧵").replace("*", "⁎").replace("|", "⏐")

fileName = f"{date} - {title}.m4a"

content = []

print("Description: ")
# Continuously get and append multi-line user input until ctrl-d or space+enter(on the last newline) is pressed
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
    # Replace double quotes with “ which is a Unicode character U+201C, the LEFT DOUBLE QUOTATION MARK.
    line = line.replace('"', '`“').replace("'", "`'")
    if line != '':
        description = description + line
    else:
        # Appends `n`n at the end of a newline so powershell can parse as two newline
        description = description + "`n`n"


# print(re.search(r'[^-\w\.]', description))
# re.sub(r'[^-\w\.]', '_', description)
#If there is an '&' then escape it using "`&" in both python and powershell
description = description.replace('&', '"`&"')
print(description)

area_id = input("X-Radiko-AreaId: ")
auth_token = input("X-Radiko-AuthToken: ")

ffmpeg_args = ['powershell.exe', '-NoExit', 'ffmpeg']
ffmpeg_args += ["-headers", f'"X-Radiko-AreaId: {area_id}"', "-headers", f'"X-Radiko-AuthToken: {auth_token}"']
# ffmpeg_args += ['-user_agent', '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"']
ffmpeg_args += ['-i', f'"{url}"', '-metadata', f'date={date}', '-metadata', f"artist='{artist}'",
                '-metadata', f'description="{description}"', '-codec', 'copy', f"'{fileName}'"]
try:
    process = subprocess.run(ffmpeg_args)
    print("Return Code:", process.returncode, process.args)
except Exception as e:
    print(e)

