import subprocess

# the m3u8 url
url = input("URL: ")
# Escape & if the url is not enclosed in double quotes
if url[0] != '"':
    url = url.replace("&", "`&")
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
# Replace / with unicode character U+29F8 ⧸ which is a unicode big solidus
# Replace ? with unicode character U+FF1F ？ which is a fullwidth question mark
# Replace \ with unicode character U+29F5 ⧵ which is a Reverse Solidus Operator
# Replace * with unicode character U+204E ⁎ which is a Low Asterisk
# Replace | with unicode character U+23D0 ⏐ which is a Vertical Line Extension
title = title.replace('"', '“').replace("<", "＜").replace(">", "＞").replace(":", "꞉").replace("/", "⧸").replace("?", "？").replace("\\", "⧵").replace("*", "⁎").replace("|", "⏐")

fileName = title + ".mkv"

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
# e.g. CloudFront-Key-Pair-Id=K33HSRY3XILYEV;CloudFront-Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly92b2QyLnNwd24uanAvc3B3bi12b2QyLzIxMTAyMTAxLWpwc3Vpc2VpL2dycDEvY2FtMV92Mi8qIiwiQ29uZGl0aW9uIjp7IklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifSwiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2Mzc1MDY3OTkwMDB9fX1dfQ_=;CloudFront-Signature=BXH4mcyB52hd-oPbeDfrJQnqEoqqwadJFYwsiuCWBmlmh2~CRN84jnBpw4f4k56wIOdIc5abH5YX8rJ70JIFeQPcosDL6gnEZ3oWtnydm2irMgN2S0OFjQlwZg1vReP2oRd4mK/+IqdcnX/QQ78hPrp98tdl5sgNtXoctmzgt+UqadgtTVgy48cL0rfAechqSUhsi2xxRbt03t36qyLabnLs/Vk1QyUgY92RiXiz7RWzp09hcclypPGVAmkXu7xJOanSl4IFU5DHYa4q3fqd2IaOInL7hl2xXPfGxVcKMFWfrTVhhlO/FCgvmZVHIUr7KtdonMzqJXGZu81IKwC+mg_=;
cookie = input("Cookies(key-value pair): ")
num_header = int(input("Number of headers: "))
if num_header != 0:
    header = []
    for num in num_header:
        header.append(rf'-headers "{input("Header(key:value pair): ")}"')

ffmpeg_args = ['powershell.exe', '-NoExit', 'ffmpeg']
if cookie is not None or cookie != "" or cookie != " ":
    ffmpeg_args += ["-headers", f'"Cookie: {cookie}"']
if num_header != 0:
    ffmpeg_args += header
# ffmpeg_args += ['-user_agent', '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"']
ffmpeg_args += ['-i', url, '-metadata', f'date={date}', '-metadata', f'artist="{artist}"', '-metadata',
                f'synopsis="{description}"', '-codec', 'copy', f'"{fileName}"']
try:
    process = subprocess.run(ffmpeg_args)
    print("Return Code:", process.returncode, process.args)
except Exception as e:
    print(e)

