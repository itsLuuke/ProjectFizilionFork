import os
import shutil

from git.exc import InvalidGitRepositoryError

from userbot import LOGS


def load_custom_modules(url: str):
	LOGS.warning("Loading custom plugins, careful using this feature as it may not be safe!")
	if not os.path.exists("userbot/custom_modules/"):
		os.makedirs("userbot/custom_modules/")

	if not os.path.exists("userbot/custom_modules/__init__.py"):
		shutil.copy("userbot/custom_modules_init.py", "userbot/custom_modules/__init__.py")

	try:
		os.system(f"git clone {url} custom_modules/")
	except InvalidGitRepositoryError:
		LOGS.error("Invalid Git repository. Please provide the URL of repository.")
		return
	for file in os.listdir("custom_modules/"):
		if file.endswith(".py") and not file.endswith("__init__.py"):
			shutil.copy("custom_modules/" + file, "userbot/custom_modules/" + file)
		elif file == "requirements.txt":
			os.system("pip3 install -r custom_modules/requirements.txt")

	LOGS.info("Custom Plugins Loaded")
