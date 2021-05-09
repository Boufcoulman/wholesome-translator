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

To make it work :
- create the "config.toml" file from "config_default.toml" file with the discord token associated with your bot.
- create the ".env" file with the absolute path to the "config.toml" file in this folder.

To go further :
- you can use the wholesome_bot.service in order to make it run as a daemon : As root, copy the file to /etc/systemd/system/wholesome_bot.service. Then change the paths of the "WorkingDirectory" and "ExecStart" lines in order to match your installation. Finally run `sudo systemctl start wholesome_bot.service` to make it pop.
