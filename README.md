# Python Size and Time Based Logging File Rotating Handler

Python logging's file based [handlers](https://docs.python.org/3/library/logging.handlers.html) have two different kinds of rotation. 
* [Size based rotation](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler)
* [Time based rotation](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler)

However, these rotations work in isolation. Only one handler can be attached to a log file.
One can only add either Size based rotation or Time based rotation.

Using `chandler.handler.SizedAndTimedRotatingHandler` you can rotate the files based on both time and size. Files will be rotated whenever either of the conditions are met.

### How to Use
 import the handler
 ```python
from chandler.handler import SizedAndTimedRotatingHandler
```

Then you can initialise your loggers and append this handler.
```python
logger = logging.getLogger('test-logger')
log_file_path = '/var/log/test/logging.log'
rotating_handler = SizedAndTimedRotatingHandler(log_file_path, when='h', interval=1, max_bytes=50000, backup_count=3)
logger.addHandler(rotating_handler)
```
In the above example the handler is configured to rotate every one hour or whenever the file size reaches 50k bytes.
This handler is built on top of [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler), so most of the arguments are similar to that of TimedRotatingFileHandler. 

### installation 
You can install with pip
```bash
$ pip install chandler
```
### Contribution


#### Authors
* [Suraj Arya](https://github.com/suraj-arya)
