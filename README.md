***Hasty***

A CLI client for hastebin-based text sharing websites.

Usage:\
hasty [-h] [-c | -f FILE] [-p]\
Grabs data from stdin (press Ctrl-D when you finish writing) and loads it on hastebin.com, returning the link\
-h, --help
-c: --copy - Uses contents of a clipboard as input\
-f: --file - Uses contents of a text file as input\
-p: --paste - Pastes the link in a clipboard instead of printing