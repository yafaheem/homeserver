# homeserver
Upload + Download Server for Home

## Running on Windows 11

If you're running the server on Windows 11 and want it to stay up in the background like a daemon, the most common approaches are:

1. **Task Scheduler** (built‑in, recommended)
   - Open Task Scheduler and create a new basic task.
   - Set the trigger to "At startup" or another schedule of your choice.
   - For the action choose "Start a program" and point it to your Python executable (e.g. `C:\Python39\python.exe`).
   - In the "Add arguments" field put the path to `app.py` (e.g. `C:\path\to\homeserver\app.py`).
   - Optionally configure "Start in" to the project directory so relative paths work.
   - On the **Settings** tab check "Run whether user is logged on or not" and "Run with highest privileges" if needed.
   - Save the task; it will execute the server automatically at boot. Logs can be viewed under Task Scheduler’s history or by redirecting output inside `app.py`.

2. **NSSM (Non‑Sucking Service Manager)**
   - Download [nssm](https://nssm.cc/) and place `nssm.exe` somewhere in your PATH.
   - Open an elevated command prompt and install the service:
     ```cmd
     nssm install homeserver "C:\Python39\python.exe" "C:\path\to\homeserver\app.py"
     ```
   - Configure log files using the NSSM GUI that appears or via command‑line arguments.
   - Start the service:
     ```cmd
     nssm start homeserver
     ```
   - The server will run as a Windows service and can be managed via `services.msc`.

3. **Manually running in a background terminal**
   - Open PowerShell and run:
     ```powershell
     Start-Process -FilePath python -ArgumentList 'C:\path\to\homeserver\app.py' -NoNewWindow -WindowStyle Hidden
     ```
   - This will launch the script detached; you can capture logs by redirecting stdout/stderr inside the script or by wrapping the call in a batch file that redirects to a file.

### Running without administrator rights

If you don't have admin privileges, the following methods work under a standard user account:

- **Startup folder or Scheduled Task (non‑elevated)**
  1. Create a shortcut or batch file pointing to `pythonw.exe C:\path\to\homeserver\app.py` and place it in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.
  2. The script will start automatically when you log in, and because `pythonw.exe` suppresses the console window it behaves like a daemon.
  3. Alternatively, use Task Scheduler as above but on the **General** tab select "Run only when user is logged on" and do **not** check "Run with highest privileges". The task will run with your normal user rights.

- **Third-party helpers**: Tools such as [nssm](https://nssm.cc/) also support creating services under a specific user account without requiring full admin access; use `nssm install homeserver ...` and choose the "Log on" tab to specify a non-admin user.

> ⚠️ These instructions target Windows 11 only. For Linux or macOS see the appropriate documentation.

---
