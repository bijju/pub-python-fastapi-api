import zipapp
import os
import shutil
import logging
import traceback
import sys
import subprocess
import toml
from datetime import datetime   



# --------------------------------------------------------------------
# Default Variables for ZipApp Build
# --------------------------------------------------------------------
program_name = os.path.basename(__file__)
version = "0.0.0"

try:
    # Read pyproject.toml to get the project info
    with open("pyproject.toml", "r") as f:
        py_project_toml = toml.load(f)
        program_name = py_project_toml["tool"]["poetry"]["name"]
        version = datetime.now().strftime("%Y.%m.%d.%H%M%S")
        if program_name is None:
            raise AttributeError("Unable to find project name in pyproject.toml")
        if version is None:
            raise AttributeError("Unable to find version in pyproject.toml")
except AttributeError:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    logging.error("Unknown AttributeError or Error occurred while reading pyproject.toml!")
    logging.error(f"Exception Type: {str(exc_type)}")
    logging.error(f"Exception Value: {exc_value}")
    logging.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)
except Exception:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    logging.error("Unknown Exception or Error occurred while reading pyproject.toml!")
    logging.error(f"Exception Type: {str(exc_type)}")
    logging.error(f"Exception Value: {exc_value}")
    logging.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)

project_name = str(os.path.basename(os.getcwd())).replace(" ", "-")
app_name = f"{project_name}-{version}.pyz"

# --------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------
build_directory = 'build'
base_dist_directory = "dist"
base_tests_directory = "tests"
base_source_directory = program_name.replace("-", "_")
lst_other_files = ["pyproject.toml", "LICENSE.txt", "README.md"]


formatter = logging.Formatter(
    '[%(asctime)s] [%(filename)s] [%(levelname)s] [%(lineno)d:%(funcName)s] >> %(message)s'
)
lg = logging.getLogger(__file__)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
lg.addHandler(ch)
lg.setLevel(logging.DEBUG)
lg.info("# =======================================================================================")
lg.info(f"# Starting Zipapp: {program_name}")
lg.info(f"# Version: {version}")
lg.info("# =======================================================================================")

# --------------------------------------------------------------------
# Zipapps build code
# --------------------------------------------------------------------
try:
    target_directory_name = base_dist_directory
    source_directory_name = base_source_directory
    tests_directory_name = base_tests_directory

    source_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), source_directory_name)
    tests_source_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        source_directory_name,
        tests_directory_name
    )
    target_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), target_directory_name)
    lg.info(f"BASE: {source_directory}")
    if not os.path.exists(source_directory):
        raise NotADirectoryError("Source directory does not exists: " + str(source_directory))
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)

    os.makedirs(target_directory)
    lg.info(f"Target Path: {target_directory}")
    lg.info(f"App Name: {app_name}")
    abs_app_path = os.path.join(target_directory, app_name)
    lg.info(f"Abs Path: {abs_app_path}")
    # sys.exit(255)

    # Clean build Directory and Recreate
    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
    os.makedirs(build_directory)
    venv_build_directory = build_directory
    
    # Copy Source from src to build_directory
    lg.info(f"Copying Source to Build Directory: {source_directory_name} -> {build_directory}")
    shutil.copytree(base_source_directory, build_directory, dirs_exist_ok=True)

    for file in lst_other_files:
        shutil.copy(file,venv_build_directory)
        
    # Install Local Requirements
    temp_src_dir = os.getcwd()
    poetry_zipapp_commands = [
        # f'cd {build_directory}',
        'python -c "import os; print(os.getcwd())"',
        'python -c "import sys;print(sys.executable)"',
        'poetry lock --verbose',
        'poetry install --compile --verbose --without test,docs',
        'poetry show --verbose',
        # 'poetry run pytest --quiet --verbose',
        # 'poetry build --verbose' # This is used for Python Wheel Package
    ]
    
    for comm in poetry_zipapp_commands:
        lg.info(f"Command: {comm}")
        p = subprocess.run(
            comm,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        lg.info(f"Return Code: {p.returncode}")
        if p.returncode != 0:
            lg.error(f"[STDERR] {p.stderr}")
            lg.error(f"Return Code: {p.returncode}")
            # Check PyTest No Tests found
            if p.returncode == 5 and "pytest" in comm:
                lg.info(f"PyTest Command Command: {comm}")
            else:
                raise RuntimeError(
                    f"[Error] Command error, Build failed, Requirement "
                    f"not installed! Command: {comm}")
        lg.info(f"[STDOUT] {p.stdout}")

    venv_dir = os.path.abspath(os.path.join(os.getcwd(), ".venv", "Lib", "site-packages"))
    lg.info(f"VENV: {venv_dir}")
    
    shutil.copytree(venv_dir, venv_build_directory, dirs_exist_ok=True)

    zipapp.create_archive(
        build_directory,
        target=abs_app_path,
        compressed=True
    )

    if os.path.isdir(build_directory):
        shutil.rmtree(build_directory)
except subprocess.CalledProcessError:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    lg.error(f"Unknown Exception or Error occurred: {str(exc_type)}")
    lg.error(f"Exception Type: {exc_type}")
    lg.error(f"Exception Value: {exc_value}")
    lg.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)
except FileNotFoundError:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    lg.error(f"Unknown Exception or Error occurred: {str(exc_type)}")
    lg.error(f"Exception Type: {exc_type}")
    lg.error(f"Exception Value: {exc_value}")
    lg.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)
except NotADirectoryError:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    lg.error(f"Unknown NotADirectoryError occurred: f{str(exc_type)}")
    lg.error(f"Exception Type: {exc_type}")
    lg.error(f"Exception Value: {exc_value}")
    lg.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)
except Exception:
    exc_type, exc_value, exec_traceback = sys.exc_info()
    lg.error("Unknown Exception or Error occurred!")
    lg.error(f"Exception Type: {str(exc_type)}")
    lg.error(f"Exception Value: {exc_value}")
    lg.error(str.join("", traceback.format_exception(exc_type, exc_value, exec_traceback)))
    sys.exit(255)
lg.info(f"Zipapp package build successful: {app_name} [Full Path: {abs_app_path}]")
lg.info("Shutting down build process!")
