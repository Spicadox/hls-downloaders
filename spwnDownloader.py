import subprocess
import re
url = input("URL: ")
title = input("Filename: ")
artist = input("Artist: ")
# e.g. 2021-10-12
date = input("Date: ")

# Replace double quotes with “ which is a Unicode character U+201C, the LEFT DOUBLE QUOTATION MARK.
title = title.replace('"', '“')

fileName = title + ".mkv"

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
    # Replace double quotes with “ which is a Unicode character U+201C, the LEFT DOUBLE QUOTATION MARK.
    line = line.replace('"', '`“')
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
# e.g. CloudFront-Key-Pair-Id=K33HSRY3XILYEV;CloudFront-Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly92b2QyLnNwd24uanAvc3B3bi12b2QyLzIxMTAyMTAxLWpwc3Vpc2VpL2dycDEvY2FtMV92Mi8qIiwiQ29uZGl0aW9uIjp7IklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifSwiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2Mzc1MDY3OTkwMDB9fX1dfQ_=;CloudFront-Signature=BXH4mcyB52hd-oPbeDfrJQnqEoqqwadJFYwsiuCWBmlmh2~CRN84jnBpw4f4k56wIOdIc5abH5YX8rJ70JIFeQPcosDL6gnEZ3oWtnydm2irMgN2S0OFjQlwZg1vReP2oRd4mK/+IqdcnX/QQ78hPrp98tdl5sgNtXoctmzgt+UqadgtTVgy48cL0rfAechqSUhsi2xxRbt03t36qyLabnLs/Vk1QyUgY92RiXiz7RWzp09hcclypPGVAmkXu7xJOanSl4IFU5DHYa4q3fqd2IaOInL7hl2xXPfGxVcKMFWfrTVhhlO/FCgvmZVHIUr7KtdonMzqJXGZu81IKwC+mg_=;
cookie = input("Cookie(CloudFront-Key-Pair-Id;CloudFront-Policy;CloudFront-Signature;): ")

ffmpeg_args = ['powershell.exe', '-NoExit', 'ffmpeg']
ffmpeg_args += ["-headers", f'"Cookie: {cookie}"']
# ffmpeg_args += ['-user_agent', '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"']
ffmpeg_args += ['-i', url, '-metadata', f'date={date}', '-metadata', f"artist='{artist}'", '-metadata', f'description="{description}"', '-codec', 'copy', f"'{fileName}'"]
try:
    process = subprocess.run(ffmpeg_args)
    print("Return Code:", process.returncode, process.args)
except Exception as e:
    print(e, process.args)

