# homeserver
Upload + Download Server for Home

This small Flask app accepts file uploads and allows you to browse/download what has been stored.

## Setup & running

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate            # on Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```

   By default it listens on `0.0.0.0:5000`.

   Optional environment variables:
   - `UPLOAD_FOLDER`: directory where uploads are stored (`uploads` by default)
   - `SECRET_KEY`: Flask secret key for session management
   - `MAX_CONTENT_LENGTH`: maximum upload size in bytes
   - `AUTH_MODE`: `none`, `token`, `password`, or `basic`
   - `UPLOAD_TOKEN`: token used when `AUTH_MODE=token`
   - `ADMIN_PASSWORD`: password used when `AUTH_MODE=password`
   - `BASIC_USERNAME`: username used when `AUTH_MODE=basic`
   - `BASIC_PASSWORD`: password used when `AUTH_MODE=basic`

After launch, open a browser to http://localhost:5000/ to upload files or
browse existing uploads.

Example auth usages:

- no auth:
  ```bash
  AUTH_MODE=none python app.py
  ```
- token auth:
  ```bash
  AUTH_MODE=token UPLOAD_TOKEN=changeme python app.py
  ```
- password auth (web login):
  ```bash
  AUTH_MODE=password ADMIN_PASSWORD=secret python app.py
  ```
- basic HTTP auth:
  ```bash
  AUTH_MODE=basic BASIC_USERNAME=admin BASIC_PASSWORD=secret python app.py
  ```

## Windows production deployment

On Windows, prefer a production WSGI server that supports native Windows such as
`waitress`. `gunicorn` is listed for Linux/Unix deployment, but it does not
support Windows.

### Install requirements

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run manually

```powershell
powershell -ExecutionPolicy Bypass -File .\run_windows.ps1 -Port 5000 -UploadFolder C:\homeserver\uploads
```

Press `Ctrl+C` to stop the server.

### Run as a Windows service or startup task

Option 1: NSSM (recommended)
- Download and install NSSM: https://nssm.cc/
- Create the service:
  1. `nssm install homeserver`
  2. Set Application path to your Python executable, e.g. `C:\Python311\python.exe`
  3. Set Arguments to `-m waitress --host=0.0.0.0 --port=5000 app:app`
  4. Set Startup directory to the repository folder.
- Start/stop:
  ```powershell
  nssm start homeserver
  nssm stop homeserver
  ```

Option 2: Task Scheduler
- Create a scheduled task triggered at startup or user logon.
- Use the same command above or call `run_windows.ps1`.
- Stop by disabling or ending the task.

Option 3: Windows service wrapper
- Use `sc.exe create` or `winsw` if you want a native Windows service.
- Example with `sc.exe`:
  ```powershell
  sc create homeserver binPath= "C:\Python311\python.exe -m waitress --host=0.0.0.0 --port=5000 app:app" start= auto
  sc start homeserver
  sc stop homeserver
  sc delete homeserver
  ```

### Recommended production command

```powershell
python -m waitress --host=0.0.0.0 --port=5000 app:app
```

This runs the Flask app with a production-ready WSGI server on Windows. The
`run_windows.ps1` helper is provided for convenient manual startup.

