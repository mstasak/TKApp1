""" TKAPP1 main startup code """

# very crude string output to debug package:class:module imports

#import sys
#raise RuntimeError(sys.path)

import logging
logger = logging.getLogger(__name__)

from lib.logger import applog
from myapp import MyApp
applog.config_logging()

logger.info("App Starting")
my_app : MyApp = MyApp()
_ = my_app.run()
logger.info("App Ended")
#print(my_app)

#must run in terminal pane else .venv must be initialized
# mypy --strict src/ lib/