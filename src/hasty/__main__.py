#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
from hasty import hasty_app, log_setup, cli, config


def main():
    """
    Parses the command line, loads the URL from config file, sets up the application and runs it
    """
    args = cli.parse_args()

    log_setup.set_logging(args.debug)
    logger = logging.getLogger(__name__)

    url = config.load_config()

    text_source = hasty_app.get_text_source(args.copy, args.file)
    link_output = hasty_app.get_link_output(args.paste)
    app = hasty_app.Hasty(url, text_source=text_source, link_output=link_output)
    logger.info(
        f"App initialised with url {url} and command line arguments: " +
        ', '.join([f'{arg} = {value}' for arg, value in vars(args).items()]))
    app.run()


if __name__ == '__main__':
    main()
