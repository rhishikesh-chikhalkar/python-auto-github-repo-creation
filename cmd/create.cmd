@echo off

set fn=%1
set flag=%2
cd /d "%~dp0\..\"

If "%1"=="" (
    echo "error"
) else ( 
    if "%2"=="g" (
        python src/remote.py %fn% %flag%
        ) else (
            if "%2"=="l" (
                python src/local.py %fn%
            )
        )
    )
