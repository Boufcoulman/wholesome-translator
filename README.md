Custom discord bot developed for a specific discord server and to make his developers increase their discord bot programming skills in a playful way !

https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
https://discordpy.readthedocs.io/en/latest/api.html


Set me up : (ubuntu 20.04)
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
sudo apt install pipenv
cd
git clone https://github.com/Boufcoulman/wholesome-translator.git
cd wholesome-translator
pipenv shell
pipenv install
```

To make it work on the hosting server :
- create the "config.toml" file from "config_default.toml" file with the discord token associated with your bot.
- create the ".env" file with the absolute path to the "config.toml" file in this folder.

To go further :
- you can use the wholesome_bot.service in order to make it run as a daemon : As root, copy the file to /etc/systemd/system/wholesome_bot.service. Then change the paths of the "WorkingDirectory" and "ExecStart" lines in order to match your installation. Finally run `sudo systemctl start wholesome_bot.service` to make it pop. You can run `sudo systemctl enable wholesome_bot.service` to make it start with the device its running on.

To make it work from [discord developer portal](https://discord.com/developers/applications) :
- use OAuth2 link with *Send Messages*, *Read Message History* and *Add Reactions* permissions as with this link from OAuth2 menu ***discord.com/api/oauth2/authorize?client_id=\<bot_id\>&permissions=67648&scope=bot***
- enable **Server Members Intent** from the bot menu
