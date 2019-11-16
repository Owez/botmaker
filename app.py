import os

def slugify(uin):
    """Slugs text"""

    return uin

def pascal_case(uin):
    """Makes text into PascalCase"""

    return uin

# Get bot name and cog file names
bot_name = input("Bot's name: ")
cmdlist = [input(f"[{i+1}]: Command name: ") for i in int(input("Number of commands: "))]

# Make bot folder & cd
os.mkdir(bot_name)
os.chdir(bot_name)

# Make cogs folder & cd
os.mkdir("cogs")
os.chdir("cogs")

for cog in cmdlist:
    with open(f"{slugify(cog})}.py", "w+") as fstream:
        pass # TODO write stuff and make classes with [pascal_case]
