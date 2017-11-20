import logging
import logging.config
import yaml


def manualConfigLogging(args):
    loglevel = args.log.upper()
    numeric_level = getattr(logging, loglevel)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=numeric_level)


def configLogging(args):
    conf = getattr(args, 'log.conf')
    if not conf:
        conf = 'etc/logging.conf'
        # conf = '/etc/text_lord.d/logging.conf'
    try:
        with open(conf, 'r') as f:
            logging.config.dictConfig(yaml.load(f))
    except FileNotFoundError:
        print('Logging config file not found')
