***Hasty***

![Python application](https://github.com/Vikdemen/hasty/workflows/Python%20application/badge.svg)

A CLI client for hastebin-based text sharing websites.

Installation: pip install git+https://github.com/Vikdemen/hasty \
Use ['testing'] if you want testing dependencies installed

Usage:\
hasty [-h] [-c | -f FILE] [-p][-d]\
Grabs data from stdin (press Ctrl-D when you finish writing) and loads it on hastebin.com, returning the link\
-h, --help
-c: --copy - Uses contents of a clipboard as input\
-f: --file - Uses contents of a text file as input\
-p: --paste - Pastes the link in a clipboard instead of printing\
-d: --debug - Outputs debugging logs

Change the link in config.ini to switch between hastebin-based sites.

Examples:\
hasty - Input the text, press Ctrl+D (Linux)/Ctrl+Z (Win) and get the link
hasty -cp - Text in your clipboard is replaced by hastebin link
hasty -f file.txt - 
echo 'hello world' | hasty - Uses the output of another command