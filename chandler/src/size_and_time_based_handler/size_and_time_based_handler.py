
import os

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class RotatingFileNamer:
    """
    Helper class used in BaseRotatingHandler
    Using this to override default settings of TimedRotatingHandler
    """

    def __call__(self, default_name):
        """

        Parameters
        ----------
        default_name: name which TimedRotatingHandler will be using for backup files
            - application.log.2022-08-29_18

        Returns str: updated name of the backup file
            - application.log.2022-08-29_18-39-19
        -------

        """
        name_parts = default_name.split('.')
        out_parts = name_parts[:-1]
        out_parts.append(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        return '.'.join(out_parts)


class SizedAndTimedRotatingHandler(TimedRotatingFileHandler):
    """
    This Handler adds Size based rotation functionality over TimedRotatingFileHandler
    Rest all logic works the same as the Base class, except the rotation happens
    also based on the size of the log files.
    max_bytes parameter will be used to compare the size after which if log file
    increases, it will be rotated.

    Another change from the TimedRotatingFileHandler is that the backup files
     are named with fully qualified datetime strings.
     Example: application.log.2022-08-29_18:25:12
    """

    # name the files with fully qualified datetime string
    # rather than just the hour or minute
    namer = RotatingFileNamer()

    def __init__(self, filename, when='h', interval=1, max_bytes=0,
                 backup_count=5, encoding=None, delay=False,
                 utc=False, at_time=None, errors=None):
        self._max_bytes = max_bytes
        TimedRotatingFileHandler.__init__(
            self, filename, when=when, interval=interval,
            backupCount=backup_count, encoding=encoding,
            delay=delay, utc=utc, atTime=at_time, errors=errors
        )
        self.backup_count = backup_count

    def shouldRolloverOnSize(self):
        """
        taken directly from the RotatingFileHandler
        Returns: boolean
        checks if should rotate the file based on the specified size
        -------
        """
        if os.path.exists(self.baseFilename) and not os.path.isfile(self.baseFilename):
            return False

        if self.stream is None:
            # returning False if stream is not defined.
            # In the RotatingFileHandler it actually opens a stream
            # however, assuming that stream will be opened by the TimedRotatingHandler
            return False

        if self._max_bytes > 0:
            self.stream.seek(0, 2)
            if self.stream.tell() >= self._max_bytes:
                return True
        return False

    def shouldRollover(self, record):
        """
        Called by the logger to check if rollover should happen.
        This method is overridden to include the functionality to check
        if we need to rotate based on size as well.
        """
        return self.shouldRolloverOnSize() or\
            super().shouldRollover(record)

    def getFilesToDelete(self):
        """
        return the list of files to be deleted after rollover
        Since we are using custom namer; we know the suffixes exactly
        """
        dir_name, base_name = os.path.split(self.baseFilename)
        files_dict = {}
        for fileName in os.listdir(dir_name):
            _, ext = os.path.splitext(fileName)
            date_str = ext.replace('.', '')
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
                files_dict[d] = fileName
            except:
                pass
        if len(files_dict) < self.backup_count:
            return []

        sorted_dict = dict(sorted(files_dict.items(), reverse=True))
        return [
                   os.path.join(dir_name, v) for k, v in sorted_dict.items()
               ][self.backup_count:]
