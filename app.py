import os
import json

def slugify(uin):
    """Slugs text"""

    return uin

def pascal_case(uin):
    """Makes text into PascalCase"""

    return uin

def get_static():
    """Gets static text from the `static/` directory"""

    file_prefix = "static/"
    output = {}

    for static_text in os.listdir(file_prefix):
        with open(file_prefix + static_text, "r") as fstream:
            output[static_text[:-4]] = fstream.read()
    
    return output

# Get essential meta about bot
bot_name = slugify(input("Bot's name: "))
description = input("Bot description (1-liner): ")
cmdlist = [input(f"[{i+1}]: Command name: ") for i in range(int(input("Number of commands: ")))]
static_text = get_static()

# Slug & pacal names
bot_slug = slugify(bot_name)
bot_pascal = pascal_case(bot_name)

# Make project folder (will be `bot_name/bot_name/__init__.py` with top-level contaning meta)
os.mkdir(bot_slug)
os.chdir(bot_slug)

# Write to README.md file in top-level
with open("README.md", "w+") as fstream:
    fstream.write(f"# {bot_name}\n\n{description}\n")

# Make bot folder & cd
os.mkdir(bot_slug)
os.chdir(bot_slug)

# Make cogs folder & cd
os.mkdir("cogs")
os.chdir("cogs")

for cog in cmdlist:
    cog_slug = slugify(cog)
    cog_pascal = pascal_case(cog)

    with open(f"{cog_slug}.py", "w+") as fstream:
        file_format = f"""from discord.ext import commands
from {bot_name}.utils import embed_generator, load_message

class {cog_pascal}(commands.Cog):
    def __init__(self, client):
        self.client = client

    # code here

def setup(client):
    client.add_cog({cog_pascal}(client))
    load_message("{cog_pascal}")
"""

        fstream.write(file_format)

# Back to top-level
os.chdir("..")

with open("utils.py", "w+") as fstream:
    fstream.write(static_text["utils.py"])
