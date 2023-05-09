# Python FastAPI API
Python Fast API Description TBD!


# Set Up Python 
- Naviget to python.org
- Download 3.11 or higher
    - Windows:Install (Follow Onscreen Instructions)
    - MacOS:Install (Follow Onscreen Instructions)
    - Linux: You are awesome, since you already have it! LINUX RULES!
    
- Using Terminal to Build and Run project:
    - Run Python Commands
        ```
        pip install poetry
        ```
        ```
        cd <Absolute-Path-To-Downloaded-Project>
        ```
        ```
        poetry init
        ```
        ```
        .venv/Scripts/activate
        ```
        - For Windows: 
            - CMD: 
            ```
            .venv/Scripts/activate.bat
            ```
            - Powershell: 
            ```
            .venv/Scripts/activate.ps1
            ```
        ```
        poetry lock
        ```
        ```
        poetry install
        ```
        ```
        python agentx-core-api/__main__.py
        ```
    - Build: This Generates ZipApp Application packed with Dependencies (mostly)
        ```
        python build.py
        ```
        - Example Output line: [2023-05-05 15:35:01,927] 
        ```
        [build.py] [INFO] [185:<module>] >> Zipapp package build successful: agentx-core-api-2023.05.05.153437.pyz [Full Path: G:\Workspace\agentx-core-api\dist\agentx-core-api-2023.05.05.153437.pyz]
        ```
        - Run ZipApp Application:
            - Hypercorn Server:
            ```
                python agentx-core-api-2023.05.05.153437.pyz --hyper
            ```
            - UVICORN Server:
            ```
                python agentx-core-api-2023.05.05.153437.pyz --uvicorn
            ```
            - Default (Hypercorn Server) \w Env Force: which will use TOML Config  in config folder: [local|dev|qa|uat|prod].toml
            ```
                python agentx-core-api-2023.05.05.153437.pyz --env [local|dev|qa|uat|prod]

            ```


# VSCode: How to Setup Python Fast API for this run
- Open VSCode Open Folder, Navigate to Debug Mode and Select Run or Build ZipApp
    - Prerequisites:
        - Install Plugins:
            - Python
            - Flake8
            - Pylance
    - You can run all the same commands as in Above terminal using VSCode Built In terminal
        - Run Python Commands
            ```
            pip install poetry
            ```
            ```
            cd <Absolute-Path-To-Downloaded-Project>
            ```
            ```
            poetry init
            ```
            ```
            .venv/Scripts/activate
            ```
            - For Windows: 
                - CMD: 
                ```
                .venv/Scripts/activate.bat
                ```
                - Powershell: 
                ```
                .venv/Scripts/activate.ps1
                ```
            ```
            poetry lock
            ```
            ```
            poetry install
            ```
    - Run 
        - Manual Right click on __main__.py and run
        - Navigate to Debugger 
            - Selection "[Run] Main App"
            - Select "Build - ZipApp File"
                - Copy ZipApp to any other location and run (Should have all dependencies packed)
                    - python agentx-core-api-2023.05.05.153437.pyz
                    - Check other options above

# how to run on inteliJ
- Run __main__.py as runconfiguration, with optional arguments

# How to Run ZipApp App
- python 
```
python agentx-core-api-<YYYY.MM.DD.HH.MI.SS.NNNNNN>.pyz --Optional <Arguments>
```