Minimal Home Upload Server

Quick start

This server now ships with a dark, mobile‑friendly web UI for easier use on phones.

- Install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Run (example, token auth):

```
export AUTH_MODE=token
export UPLOAD_TOKEN=mysupersecret
export UPLOAD_FOLDER=uploads
python app.py
```

Open http://YOUR_PC:5000 on your phone's browser (same network) and upload.  Once a file is stored you can click "Browse existing uploads" on the home page to navigate folders and retrieve files.

Authentication options

- none (AUTH_MODE=none)
  - No authentication. Useful on trusted LAN but not recommended otherwise.

- token (AUTH_MODE=token)
  - A single shared token. Set `UPLOAD_TOKEN`. Mobile uploads can send the token in the `X-UPLOAD-TOKEN` header or as `?token=` query param. Works well for simple scripts or widgets on phones.

- password (AUTH_MODE=password)
  - A simple web password. Set `ADMIN_PASSWORD`. Users sign in at `/login` and get a session cookie. Good for interactive browser uploads.

Security notes

- This server is intentionally minimal. For exposure to untrusted networks, run behind an HTTPS reverse proxy (Caddy/Nginx) and/or use a VPN.
- Consider firewall rules to restrict external access.

Examples

- Upload with curl and token header:

```
curl -H "X-UPLOAD-TOKEN: mytoken" -F "file=@photo.jpg" http://YOUR_PC:5000/upload
```

- Upload with curl and query token:

```
curl -F "file=@photo.jpg" "http://YOUR_PC:5000/upload?token=mytoken"
```

Files

- app.py: main Flask app
- templates/: upload UI and login
- requirements.txt: Python deps

