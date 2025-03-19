from lib.guiframework import AppBase
from lib.guiframework import AppPageBase
#import guiframework
from mymainpage import MyMainPage

class MyApp(AppBase):
    """App subclass, with customizations for this application"""
    def __init__(self) -> None:
        super().__init__()
        self.app_name = "TKApp1"
        #self._default_position = [0, 0]
        #self._default_size = [1024, 768]
        self.main_page: AppPageBase = MyMainPage(self.root)
    
