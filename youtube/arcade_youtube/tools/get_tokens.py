from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_tokens(client_secrets_file):
    """Get OAuth tokens using the client secrets file."""
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=SCOPES)

    # This will open a browser window for authentication
    credentials = flow.run_local_server(port=0)

    # Print the tokens in a format ready for .env file
    print("\nAdd these to your .env file:")
    print(f"YOUTUBE_TEST_TOKEN={credentials.token}")
    print(f"YOUTUBE_TEST_REFRESH_TOKEN={credentials.refresh_token}")
    print(f"YOUTUBE_TEST_CLIENT_ID={credentials.client_id}")
    print(f"YOUTUBE_TEST_CLIENT_SECRET={credentials.client_secret}")
    print(f"YOUTUBE_TEST_TOKEN_URI={credentials.token_uri}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python get_tokens.py path/to/client_secrets.json")
        sys.exit(1)

    get_tokens(sys.argv[1])
