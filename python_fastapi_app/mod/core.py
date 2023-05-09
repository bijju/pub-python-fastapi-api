import getopt
import logging
import os
from pathlib import Path
import re
import socket
import sys
import yaml
import pkg_resources
import toml
import trio
import uvicorn
from hypercorn.config import Config
from hypercorn.trio import serve
from mod.fast import app


class Core:
    """Core class
    """
    hostname = socket.gethostname()
    root_file_obj = __name__
    root_package_obj = __file__
    root_directory = os.path.dirname(__file__)
    app_config = {}
    app_environment = os.environ.get("APP_ENVIRONMENT").lower()
    is_pyz = False
    logging_config = {}
    env_override = None

    serve_type = "hypercorn"
    serve_types = {
        "hypercorn",
        "uvicorn"
    }

    def __init__(
            self, 
            root_file_obj,
            root_package_obj,
            root_directory
        ):
        self.root_file_obj = root_file_obj
        self.root_package_obj = root_package_obj
        self.root_directory = root_directory
        self.parse_args()
        if re.search(".pyz", str(sys.argv[0])):
            self.is_pyz = True
        self.load_config()
        logging.info(f"App Config: {self.app_config}")
        self.setup_logging()
    
    def parse_args(self):
        """
        Parse command line arguments
        """
        (opts, args) = getopt.getopt(
            sys.argv[1:],
            "",
            [
                "help",
                "env=", # Easiliy OVerride Environment Variables "APP_ENVIRONMENT" example: app.pyz --env=qa
                "hypercorn",
                "uvicorn"
            ]
        )

        for o, a in opts:
            if o in "--help":
                self.usage()
                sys.exit()
            elif o in "--env":
                self.env_override = a
            elif o in "--hypercorn":
                self.serve_type = "hypercorn"
            elif o in "--uvicorn":
                self.serve_type = "uvicorn"

    def load_config(self):
        """
        Load app config
        """
        config_file = f"{self.app_environment}.toml"

        # Override Environment Variables
        if self.env_override:
            config_file = f"{self.env_override}.toml"
        
        if self.is_pyz:
            logging.info("[Pre-Initialization] [ZipApp] Attempting to load TOML Config from package")
            config_str = pkg_resources.resource_stream(
                self.root_file_obj,
                f'config/{config_file}'
            ).read().decode()
            self.app_config = toml.loads(config_str)
            self.logging_config = yaml.safe_load(
                pkg_resources.resource_stream(
                    self.root_file_obj
                    , self.app_config["logging"]["log_config"]
                ).read().decode()
            )
        else:
            abs_toml_config_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(self.root_package_obj),
                    "config",
                    config_file
                )
            )
            logging.info(f"[Pre-Initialization] TOML Config: \n{abs_toml_config_path}")
            # Check File Exists
            if not Path(abs_toml_config_path).is_file():
                logging.error(f"File does not exist or PATH is incorrect: {abs_toml_config_path}")
                sys.exit(255)
            logging.info("[Pre-Initialization] [__main__] Attempting to load TOML Config from directory")
            self.app_config = toml.load(abs_toml_config_path)
            # Import Log Configuration YAML file
            with open(self.app_config["logging"]["log_config"], 'r') as stream:
                self.logging_config = yaml.load(
                    stream,
                    Loader=yaml.FullLoader
                )
        logging.info(f"App Config: {self.app_config}")

    def setup_logging(self):
        """
            Logging Setup
        """
        logging.config.dictConfig(self.logging_config)
        logging.info("Logging YAML Config Loaded!")

    def usage(self) -> None:
        """Usage.
        :description: Helper command
        :return:
        """
        logging.info("""
        App.pyz --some options (UPDATE THIS FOR YOUR APP!)
        Examples:
            $> python App.pyz --some options
        """)
    
    def is_pyz(self) -> bool:
        return self.is_pyz
    
    def run(self):
        if self.serve_type == "hypercorn":
            self.run_hypercorn()
        elif self.serve_type == "uvicorn":
            self.run_uvicorn()
        else:
            logging.error(f"Invalid Serve Type: {self.serve_type}")
            sys.exit(255)
    
    def run_hypercorn(self):
        """
        Run Hypercorn
        """
        hyper_port = 5050
        hyper_config = Config()
        if "hypercorn" in self.app_config:
            if "port" in self.app_config["hypercorn"]:
                hyper_port = self.app_config["hypercorn"]["port"]
            if "sslcertfile" in self.app_config["hypercorn"]:
                hyper_config.certfile = self.app_config["hypercorn"]["sslcertfile"]
            if "sslkeyfile" in self.app_config["hypercorn"]:
                hyper_config.keyfile = self.app_config["hypercorn"]["sslkeyfile"]
            if "sslkeyfilepwd" in self.app_config["hypercorn"]:
                hyper_config.keyfile_password = self.app_config["hypercorn"]["sslkeyfilepwd"]
        
        hyper_config.bind = f"{self.hostname}:{hyper_port}"
        trio.run(serve, app, hyper_config)

    def run_uvicorn(self):
        """
        Run uvicorn
        """
        uvi_port = 5050
        uvi_ssl_cert_file = None
        uvi_ssl_key_file = None
        uvi_ssl_key_file_pwd = None
        if "uvicorn" in self.app_config:
            if "port" in self.app_config["uvicorn"]:
                uvi_port = self.app_config["uvicorn"]["port"]
            if "sslcertfile" in self.app_config["hypercorn"]:
                uvi_ssl_cert_file = self.app_config["hypercorn"]["sslcertfile"]
            if "sslkeyfile" in self.app_config["hypercorn"]:
                uvi_ssl_key_file = self.app_config["hypercorn"]["sslkeyfile"]
            if "sslkeyfilepwd" in self.app_config["hypercorn"]:
                uvi_ssl_key_file_pwd = self.app_config["hypercorn"]["sslkeyfilepwd"]

        if uvi_ssl_cert_file and uvi_ssl_key_file and uvi_ssl_key_file_pwd:
            uvicorn.run(
                "fast:app"
                , host=self.hostname
                , port=int(uvi_port)
                , reload=True
                , log_config=dict(self.logging_config)
                , ssl_keyfile=uvi_ssl_key_file
                , ssl_certfile=uvi_ssl_cert_file
                , ssl_keyfile_password=uvi_ssl_key_file_pwd
                # , ssl_ca_certs = ssl_key_file
            )
        else:
            uvicorn.run(
                "fast:app"
                , host=self.hostname
                , port=int(uvi_port)
                , reload=True
                , log_config=dict(self.logging_config)
            )
        
        
