@ECHO OFF 
cls

TITLE File-Move-Testing

:: Set date with format YYYYMMDD
set currentDate=%date:~10,4%%date:~4,2%%date:~7,2%

:: Set directory to scan
set currentDirectory=mydir
ECHO ============================
echo Current Date : %currentDate%
echo Current Directory : %CD%\%currentDirectory%
ECHO ============================
echo.
for %%J in (TYPE1 TYPE2 TYPE3 TYPE4) do (
  echo.
  echo Checking Files Type : %%J ...
  ECHO ============================
  FOR %%I in (%currentDirectory%\*%%J_%currentDate%*.txt) DO (
    echo %%I
    :: Do your copy command or action here
  ) 
)


PAUSE
