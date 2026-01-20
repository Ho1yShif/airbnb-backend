#!/usr/bin/env python
"""
Lightweight smoke check for admin and user-preferences endpoints.
Uses urllib to avoid external dependencies.
"""
import os
import sys
import base64
from urllib import request, error

BASE_URL = os.environ.get("SMOKE_BASE_URL", "http://localhost:8000")
ADMIN_USER = os.environ.get("SMOKE_ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("SMOKE_ADMIN_PASS", "admin123456")


def fetch(path, auth=False):
    url = f"{BASE_URL.rstrip('/')}{path}"
    req = request.Request(url)
    if auth:
        token = base64.b64encode(f"{ADMIN_USER}:{ADMIN_PASS}".encode()).decode()
        req.add_header("Authorization", f"Basic {token}")
    try:
        with request.urlopen(req, timeout=10) as resp:
            body = resp.read(300)
            return resp.status, body
    except error.HTTPError as e:
        return e.code, e.read(300)
    except Exception as exc:  # noqa: BLE001
        return None, str(exc).encode()


def main():
    checks = [
        {"name": "admin", "path": "/admin/", "auth": False},
        {"name": "preferences", "path": "/api/user-preferences/current_preferences/", "auth": True},
    ]
    failed = False
    for check in checks:
        status, body = fetch(check["path"], auth=check["auth"])
        label = check["name"]
        if status and 200 <= status < 400:
            print(f"✓ {label}: HTTP {status}")
        else:
            failed = True
            print(f"✗ {label}: status={status} body={body.decode(errors='ignore')}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
