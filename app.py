import os
import json

def snakeify(uin):
    """Converts text to snake_case"""

    out = ""
    repeated = False
    spacing = (" ", "_", "-")

    for ind, i in enumerate(uin):
        if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- ":
            continue
        elif i in spacing:
            if repeated:
                continue

            out += "_"
            repeated = True
        else:
            out += i
            repeated = False
    
    return out.lower()

def pascal_case(uin):
    """Converts text into PascalCase"""

    out = ""
    should_start = True
    should_cap = False

    for ind, i in enumerate(uin):
        if i not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_- ":
            continue
        if should_start:
            out += i.upper()
            should_start = False
        elif i in ("-", "_", " "):
            should_cap = True
        elif should_cap:
            out += i.upper()
            should_cap = False
        else:
            out += i
    
    return out

def get_static():
    """Gets static text from the `static/` directory"""

    file_prefix = "static/"
    output = {}

    for static_text in os.listdir(file_prefix):
        with open(file_prefix + static_text, "r") as fstream:
            output[static_text[:-4]] = fstream.read()
    
    return output

# Get essential meta about bot
bot_name = input("Bot's name: ")
bot_prefix = input("Bot's prefix: ")[0]
description = input("Bot description (1-liner): ")
cmdlist = [input(f"[{i+1}] Command name: ") for i in range(int(input("Number of commands: ")))]
static_text = get_static()

# Slug & pacal names
bot_slug = snakeify(bot_name)
bot_pascal = pascal_case(bot_name)

# Make project folder (will be `bot_name/bot_name/__init__.py` with top-level contaning meta)
os.mkdir(bot_slug)
os.chdir(bot_slug)

# Write to README.md file in top-level folder
with open("README.md", "w+") as fstream:
    cog_names = "\n".join([f"- **{pascal_case(i)}** (`{snakeify(i)}`)" for i in cmdlist])
    readme_run = static_text["readme_run"]
    readme_contents = f"# {bot_name}\n\n{description}\n\n## Cogs\n\n{cog_names}\n\n{readme_run}"
    fstream.write(readme_contents)

# Dump simple config
json.dump({"prefix": bot_prefix}, open("config.json", "w+"))

# Write to app.py file in top-level folder
with open("app.py", "w+") as fstream:
    fstream.write(f"from {bot_slug} import client, bot_config\n\nclient.run(bot_config.TOKEN)\n")

# Make bot folder & cd
os.mkdir(bot_slug)
os.chdir(bot_slug)

# Write to __init__.py file in bot folder
with open("__init__.py", "w+") as fstream:
    init_file = f"from {bot_slug}.utils import Config, get_cogs\n" + static_text["__init__.py"]
    fstream.write(init_file)

# Add utils.py
with open("utils.py", "w+") as fstream:
    fstream.write(static_text["utils.py"])

# Make cogs folder & cd
os.mkdir("cogs")
os.chdir("cogs")

for cog in cmdlist:
    cog_slug = snakeify(cog)
    cog_pascal = pascal_case(cog)

    with open(f"{cog_slug}.py", "w+") as fstream:
        file_format = f"""from discord.ext import commands
from {bot_slug}.utils import embed_generator, load_message

class {cog_pascal}(commands.Cog):
    def __init__(self, client):
        self.client = client

    # code here

def setup(client):
    client.add_cog({cog_pascal}(client))
    load_message("{cog_pascal}")
"""

        fstream.write(file_format)
