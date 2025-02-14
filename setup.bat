@echo off
echo Setting up the project...
python -m venv .venv
echo .venv created


call .venv\Scripts\activate.bat
echo .venv activated.

python.exe -m pip install --upgrade pip
echo pip upgrade -- done

echo Installing dependencies...
pip install -r requirements.txt
echo requirements installed





:: Create and configure .gitignore
echo Creating .gitignore file...

(
    echo .venv/
    echo __pycache__/
    echo *.pyc
    echo *.pyo
    echo *.log
    echo db.sqlite3
    echo .env
    echo .idea/
    echo .vscode/
    echo .DS_Store
) > .gitignore

echo .gitignore file created.

echo.
echo Setup complete! Now you can run the server using run_server.bat

pause