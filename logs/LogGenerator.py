"""
This is just a simple handler class to help configure our logger.

It has been set up to always save the textual log output to the same
directory as this module.

We could make the class much more flexible, but its not really necessary;
we aren't really going to change the settings that often.
"""
__author__ = 'donal'
__project__ = 'Skeleton_Flask_v11'
import logging
import logging.config
import os


# ================================
# LOGGER CLASS
# ================================
class GenLogger(object):
    """
    Based on http://docs.python.org/howto/logging.html#configuring-logging
    """
    def __init__(self, output_log):
        self.output_log = '{0}/{1}'.format(
            os.path.dirname(__file__), output_log)
        logging.config.dictConfig(self.create_settings())
        self.logger = logging.getLogger(__project__)

    def create_settings(self):
        logsettings = {
            "version": 1,
            "handlers": {
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "myFormatter",
                    "filename": self.output_log
                }
            },
            "loggers": {
                __project__: {
                    "level": "DEBUG",
                    "handlers": ["fileHandler"]
                }
            },
            "formatters": {
                "myFormatter": {
                    "format": ("%(asctime)s.%(msecs).12d - %(name)s - "
                               "%(filename)s, #%(lineno)d - %(levelname)s "
                               "- %(message)s"),
                    "datefmt": "%Y-%b-%d %H:%M:%S"
                }
            }
        }
        return logsettings


if __name__ == '__main__':
    lg = GenLogger('test.log')
    lg.logger.info('this is a test')
