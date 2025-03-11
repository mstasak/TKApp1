""" TKAPP1 main startup code """

#import sys
#raise RuntimeError(sys.path)

from myapp import MyApp


my_app : MyApp = MyApp()
_ = my_app.run()
#print(my_app)

#must run in terminal pane else .venv must be initialized
# mypy --strict src/ lib/