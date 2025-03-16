import logging
logger = logging.getLogger(__name__)

def config_logging() -> None:
    logging.basicConfig(filename="TKAPP1.log", encoding="utf-8", filemode="w", level=logging.INFO,
                        format="%(asctime)22s  -  %(name)-35s  -  %(levelname)8s:  %(message)s")
    logger.info("Logger initialized.")


# class AppLog:
#     """ App-wide logging service """

#     # app_name: str = "(undefined)"
#     # _default_position = [0, 0]
#     # _default_size = [800, 600]

#     app_logger: logging.Logger

#     def __init__() -> None:
#         # self.root = tk.Tk()
#         logger = logging.getLogger()
#         logging.basicConfig("TKAPP1")
#         AppLog.app_logger = logger
#         logger.info("TKAPP1 logger initialized.")
#         logger.info("TKApp1 handle [lib.logger.]AppLog.app_logger created")

    # def run(self) -> bool : 
    #     self._load_page(self._main_page)
    #     self.root.mainloop()
    #     self._unload_page()
    #     return True
        
    # def _load_page(self, page: AppPageBase) -> None:
    #     self.root.frame = page.buildpage()

    # def _unload_page(self) -> None:
    #     self.root.frame = None
        
   