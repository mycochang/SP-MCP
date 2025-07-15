@echo off
setlocal enabledelayedexpansion

echo ============================================
echo Super Productivity MCP Bridge Setup
echo ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

:: Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed or not in PATH
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo Installing MCP dependencies...
pip install mcp

if %errorlevel% neq 0 (
    echo ERROR: Failed to install MCP dependencies
    pause
    exit /b 1
)

:: Create AppData directory
set "MCP_DIR=%APPDATA%\super-productivity-mcp"
echo Creating MCP directory: %MCP_DIR%
if not exist "%MCP_DIR%" mkdir "%MCP_DIR%"
if not exist "%MCP_DIR%\plugin_commands" mkdir "%MCP_DIR%\plugin_commands"
if not exist "%MCP_DIR%\plugin_responses" mkdir "%MCP_DIR%\plugin_responses"

:: Copy MCP server to AppData directory
echo Copying MCP server...
copy /Y "mcp_server.py" "%MCP_DIR%\mcp_server.py"
copy /Y "merge_config.py" "%MCP_DIR%\merge_config.py"

:: Create start script
echo Creating start script...
(
echo @echo off
echo echo Starting Super Productivity MCP Server...
echo cd /d "%MCP_DIR%"
echo python mcp_server.py
echo pause
) > "%MCP_DIR%\start_mcp_server.bat"

:: Configure Claude Desktop
set "CLAUDE_CONFIG=%APPDATA%\Claude\claude_desktop_config.json"
echo Configuring Claude Desktop...

:: Create Claude config directory if it doesn't exist
if not exist "%APPDATA%\Claude" mkdir "%APPDATA%\Claude"

:: Check if config file exists and merge
if exist "%CLAUDE_CONFIG%" (
    echo Backing up existing Claude config...
    copy /Y "%CLAUDE_CONFIG%" "%CLAUDE_CONFIG%.backup"
    
    echo WARNING: Existing Claude Desktop config found!
    echo This script will ADD super-productivity to your existing MCP servers.
    echo Your existing MCP servers will be preserved.
    echo.
    echo Merging with existing Claude Desktop configuration...
    
    python "%MCP_DIR%\merge_config.py" "%CLAUDE_CONFIG%" "%MCP_DIR%"
    
    if %errorlevel% neq 0 (
        echo ERROR: Failed to merge configuration. Your backup is at %CLAUDE_CONFIG%.backup
        echo Please manually add this to your Claude Desktop config:
        echo.
        echo   "super-productivity": {
        echo     "command": "python",
        echo     "args": ["%MCP_DIR%\mcp_server.py"]
        echo   }
        echo.
        pause
        exit /b 1
    )
) else (
    echo Creating new Claude Desktop configuration...
    (
    echo {
    echo   "mcpServers": {
    echo     "super-productivity": {
    echo       "command": "python",
    echo       "args": ["%MCP_DIR%\mcp_server.py"]
    echo     }
    echo   }
    echo }
    ) > "%CLAUDE_CONFIG%"
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Install the plugin in Super Productivity:
echo    - Open Super Productivity
echo    - Go to Settings ^> Plugins
echo    - Click "Upload Plugin"
echo    - Select the plugin.js file from this folder
echo.
echo 2. Restart Claude Desktop to load the MCP server
echo.
echo 3. Test the integration by asking Claude to:
echo    "Create a task in Super Productivity"
echo.
echo MCP Server installed at: %MCP_DIR%
echo Claude config updated at: %CLAUDE_CONFIG%
echo.
echo Press any key to exit...
pause >nul