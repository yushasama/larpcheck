@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT_DIR=%%~fI"

pushd "%SCRIPT_DIR%" >nul || exit /b 1

uv run --project "%ROOT_DIR%\backend\src" --with pyinstaller pyinstaller ^
  --onefile ^
  --noconsole ^
  --name LarpCheck ^
  --add-data "%ROOT_DIR%\backend\src\ransomware\resources\problems;resources/problems" ^
  --add-data "%ROOT_DIR%\backend\src\problem_bank\testcases;testcases" ^
  --add-data "%ROOT_DIR%\sandbox_backup;sandbox_backup" ^
  "%ROOT_DIR%\backend\src\ransomware\__main__.py"

set "EXIT_CODE=%ERRORLEVEL%"
popd >nul
if not "%EXIT_CODE%"=="0" exit /b %EXIT_CODE%

echo Done. dist/LarpCheck.exe ready.
endlocal
