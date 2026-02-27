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

   By default it listens on `0.0.0.0:5000`. You can control behaviour via environment
   variables documented in `app.py` (e.g. `UPLOAD_FOLDER`, `AUTH_MODE`).

After launch, open a browser to http://localhost:5000/ to upload files or
browse existing uploads.

For lightweight deployment run the script inside your preferred process supervisor
(e.g. systemd, docker, Task Scheduler on Windows, etc.).  The specifics of
running as a daemon are outside the scope of this README.

