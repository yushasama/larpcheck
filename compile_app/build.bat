@echo off
uv run pyinstaller ^
  --onefile ^
  --noconsole ^
  --name LarpCheck ^
  --add-data "backend/src/ransomware/resources/problems;resources/problems" ^
  --add-data "backend/src/problem_bank/testcases;testcases" ^
  backend/src/ransomware/__main__.py

echo Done. dist/LarpCheck.exe ready.