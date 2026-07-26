#!/usr/bin/env python3
"""Headless Google Search Console API client for the gsc-admin skill.

Covers sitemap status/resubmission, coverage/indexing (URL inspection), and
search analytics (query/CTR) for Kasper's four verified properties. Does NOT
cover manual actions/security issues -- there is no API for that; the
gsc-admin skill drives narrow browser automation for that one check.

One-time setup (see the gsc-admin SKILL.md "Access" section for full steps):
  1. Create a GCP project, enable the Search Console API, configure + publish
     an OAuth consent screen, create an OAuth client (Desktop app type).
  2. Save the downloaded client secret as credentials/client_secret.json.
  3. Run: python3 gsc_api.py --setup
     This runs the one-time interactive OAuth consent flow and writes
     credentials/token.json. Never needed again unless the token is revoked.

Usage:
  python3 gsc_api.py --setup
  python3 gsc_api.py <site_url> sitemaps
  python3 gsc_api.py <site_url> submit-sitemap <feed_path>
  python3 gsc_api.py <site_url> inspect <page_url>
  python3 gsc_api.py <site_url> analytics <start_date> <end_date> [dimension ...]

All commands print JSON to stdout. Errors go to stderr with a clear,
actionable message -- never a raw stack trace as the primary output.
"""

import argparse
import json
import sys
from pathlib import Path

CREDENTIALS_DIR = Path(__file__).resolve().parent.parent / "credentials"
CLIENT_SECRET_PATH = CREDENTIALS_DIR / "client_secret.json"
TOKEN_PATH = CREDENTIALS_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/webmasters"]

KNOWN_PROPERTIES = {
    "sc-domain:landsvig.com",
    "sc-domain:aiauto.dk",
    "sc-domain:koalafilm.dk",
    "sc-domain:vibetrends.dk",
}


def _fail(message):
    print(f"gsc-admin error: {message}", file=sys.stderr)
    sys.exit(1)


def _validate_site_url(site_url):
    if site_url not in KNOWN_PROPERTIES:
        _fail(
            f"'{site_url}' is not one of the four known properties "
            f"({', '.join(sorted(KNOWN_PROPERTIES))}). Refusing to call the "
            "API against an unrecognized property -- check for a typo."
        )


def get_credentials():
    """Load and refresh credentials, persisting the refreshed token.

    Raises a clear, actionable error (not a stack trace) if the token is
    missing, invalid, or revoked -- the most likely failure if the OAuth
    consent screen was left in Testing status during setup.
    """
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
    except ImportError:
        _fail(
            "google-auth is not installed. Run: "
            "pip3 install google-auth google-auth-oauthlib google-api-python-client"
        )

    if not TOKEN_PATH.exists():
        _fail(
            f"No token found at {TOKEN_PATH}. Run 'python3 gsc_api.py --setup' "
            "first to complete the one-time OAuth consent flow."
        )

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as exc:  # refresh token revoked, expired, or invalid
            _fail(
                "Token refresh failed -- the stored credentials are no longer "
                "valid (commonly: the OAuth consent screen was left in "
                "'Testing' status, which forces refresh tokens to expire "
                "after 7 days, or access was revoked). Re-run "
                f"'python3 gsc_api.py --setup' to re-authorize. ({exc})"
            )
        TOKEN_PATH.write_text(creds.to_json())

    if not creds or not creds.valid:
        _fail(
            "Credentials are invalid and could not be refreshed. Re-run "
            "'python3 gsc_api.py --setup'."
        )

    return creds


def run_setup():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        _fail(
            "google-auth-oauthlib is not installed. Run: "
            "pip3 install google-auth google-auth-oauthlib google-api-python-client"
        )

    if not CLIENT_SECRET_PATH.exists():
        _fail(
            f"No client secret found at {CLIENT_SECRET_PATH}. Create a GCP "
            "project, enable the Search Console API, configure + publish an "
            "OAuth consent screen, create a Desktop-app OAuth client, and "
            "download the client secret JSON to that path first."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    print(f"Setup complete. Token saved to {TOKEN_PATH}.")


def _build_service(api_name, api_version, creds):
    try:
        from googleapiclient.discovery import build
    except ImportError:
        _fail(
            "google-api-python-client is not installed. Run: "
            "pip3 install google-auth google-auth-oauthlib google-api-python-client"
        )
    return build(api_name, api_version, credentials=creds)


def list_sitemaps(site_url):
    _validate_site_url(site_url)
    creds = get_credentials()
    service = _build_service("webmasters", "v3", creds)
    result = service.sitemaps().list(siteUrl=site_url).execute()
    return result.get("sitemap", [])


def submit_sitemap(site_url, feed_path):
    """Write operation -- the only mutating call this client exposes.

    Callers (the gsc-admin skill) must only invoke this for the
    boundary-approved sitemap-resubmission case, never as a general-purpose
    write. This function does not itself enforce that boundary -- that is
    the skill's responsibility, per the plan's guardrails.
    """
    _validate_site_url(site_url)
    creds = get_credentials()
    service = _build_service("webmasters", "v3", creds)
    service.sitemaps().submit(siteUrl=site_url, feedpath=feed_path).execute()
    return {"submitted": feed_path, "site": site_url}


def inspect_url(site_url, page_url):
    _validate_site_url(site_url)
    creds = get_credentials()
    service = _build_service("searchconsole", "v1", creds)
    body = {"inspectionUrl": page_url, "siteUrl": site_url}
    return service.urlInspection().index().inspect(body=body).execute()


def query_search_analytics(site_url, start_date, end_date, dimensions):
    _validate_site_url(site_url)
    creds = get_credentials()
    service = _build_service("webmasters", "v3", creds)
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions or ["query"],
    }
    result = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows = result.get("rows", [])
    if not rows:
        return {
            "rows": [],
            "note": (
                "No rows returned. If this date range is before ~mid-July "
                "2026, that's expected -- query/CTR data only started "
                "accumulating then for these DNS-verified domains. Treat "
                "empty data from earlier ranges as expected, not an error."
            ),
        }
    return {"rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--setup", action="store_true", help="Run one-time OAuth setup")
    parser.add_argument("site_url", nargs="?", help="e.g. sc-domain:landsvig.com")
    parser.add_argument("operation", nargs="?", choices=["sitemaps", "submit-sitemap", "inspect", "analytics"])
    parser.add_argument("args", nargs="*")
    parsed = parser.parse_args()

    if parsed.setup:
        run_setup()
        return

    if not parsed.site_url or not parsed.operation:
        parser.error("site_url and operation are required unless --setup is passed")

    if parsed.operation == "sitemaps":
        result = list_sitemaps(parsed.site_url)
    elif parsed.operation == "submit-sitemap":
        if not parsed.args:
            parser.error("submit-sitemap requires a feed_path argument")
        result = submit_sitemap(parsed.site_url, parsed.args[0])
    elif parsed.operation == "inspect":
        if not parsed.args:
            parser.error("inspect requires a page_url argument")
        result = inspect_url(parsed.site_url, parsed.args[0])
    elif parsed.operation == "analytics":
        if len(parsed.args) < 2:
            parser.error("analytics requires start_date and end_date arguments")
        start_date, end_date = parsed.args[0], parsed.args[1]
        dimensions = parsed.args[2:] or None
        result = query_search_analytics(parsed.site_url, start_date, end_date, dimensions)
    else:
        parser.error(f"Unknown operation: {parsed.operation}")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
