#!/usr/bin/env python3
"""
Simple integration test for GitHub Pages site
- Verifies key URLs return HTTP 200
- Optionally checks for basic Just the Docs markup
- Exits non-zero on failure

Usage:
  BASE_URL=https://cloudshare360.github.io/aws-devops-gitlab-cicd-spring-boot-angular-fargate/ \
    python3 scripts/integration_tests/check_site.py
"""
import os
import sys
import time
import json
from urllib.parse import urljoin

import requests

DEFAULT_PATHS = [
    "",  # homepage (redirects to learning path)
    "learning-path/",
    "learning-path/foundations/",
    "learning-path/security/",
    "learning-path/security/aws-waf-deep-dive/",
    "learning-path/foundations/spring-boot-containerization/",
    "learning-path/cicd/",
]

EXPECTED_MARKERS = [
    # Common Just the Docs markers
    "just-the-docs",  # CSS class/asset name
    "site-nav",       # left nav container
]

TIMEOUT = int(os.getenv("TIMEOUT", "10"))
RETRIES = int(os.getenv("RETRIES", "5"))
SLEEP_BETWEEN = int(os.getenv("RETRY_DELAY", "3"))


def fetch(url: str) -> requests.Response:
    return requests.get(url, timeout=TIMEOUT, allow_redirects=True)


def check_url(base: str, path: str):
    url = urljoin(base, path)
    res = fetch(url)
    ok = (200 <= res.status_code < 300)
    details = {
        "url": url,
        "status": res.status_code,
        "ok": ok,
    }
    if ok:
        content = res.text.lower()
        details["has_markers"] = {m: (m in content) for m in EXPECTED_MARKERS}
    return ok, details


def wait_until_live(base: str) -> bool:
    # Try homepage first with retries (propagation delay)
    for i in range(RETRIES):
        try:
            res = fetch(base)
            if res.status_code in (200, 301, 302):
                return True
        except Exception:
            pass
        time.sleep(SLEEP_BETWEEN)
    return False


def main():
    base_url = os.getenv(
        "BASE_URL",
        "https://cloudshare360.github.io/aws-devops-gitlab-cicd-spring-boot-angular-fargate/"
    )
    if not base_url.endswith("/"):
        base_url += "/"

    results = {"base_url": base_url, "checks": []}

    if not wait_until_live(base_url):
        print(json.dumps({"error": "Site not live yet", **results}, indent=2))
        return 2

    overall_ok = True

    for path in DEFAULT_PATHS:
        try:
            ok, details = check_url(base_url, path)
            results["checks"].append(details)
            if not ok:
                overall_ok = False
        except Exception as e:
            overall_ok = False
            results["checks"].append({
                "url": urljoin(base_url, path),
                "ok": False,
                "error": str(e),
            })

    print(json.dumps(results, indent=2))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
