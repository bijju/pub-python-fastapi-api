import os
import logging.config
import logging
from mod.core import Core


class App:
    """App class
    """
    root_file_obj = __name__
    root_package_obj = __file__
    root_directory = os.path.dirname(__file__)
    
    def main(self):
        """
        Main function
        """
        logging.basicConfig(level="INFO", format="[BaseConfig] %(asctime)s - <PID %(process)d:%(processName)s> - %(pathname)s:%(lineno)d - %(funcName)s:%(lineno)d - %(name)s - %(levelname)s: %(message)s")
        logging.info("Initialising App:.....")
        core_inst = Core(
            root_file_obj = self.root_file_obj,
            root_package_obj = self.root_package_obj,
            root_directory = self.root_directory
        )
        logging.info(f"Env: {core_inst.app_environment}")
        core_inst.run()
        logging.info("Shutting down App:.....")
