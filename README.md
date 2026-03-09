# Delete Old Gmail Emails — Bulk Cleanup Script

A Python script that uses the Gmail API to permanently delete all emails older than N months from your Gmail account. Uses batch deletion for speed — can clear tens of thousands of emails in minutes.

## Project Structure

```
delete-old-mails/
├── credentials.json      # OAuth credentials (you create this)
├── token.json            # Auto-generated after first auth
├── requirements.txt      # Python dependencies
├── run.py                # The deletion script
└── README.md             # This file
```

## Prerequisites

- Python 3.7+
- A Google account with Gmail
- Google Chrome (for the OAuth consent flow)

## Setup Guide

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Click the project dropdown at the top and select **New Project**.
3. Name it something like `delete-old-mails` and click **Create**.
4. Make sure the new project is selected in the dropdown.

### 2. Enable the Gmail API

1. In the Cloud Console, go to **APIs & Services → Library** (or search "Gmail API" in the top search bar).
2. Find **Gmail API** and click **Enable**.

### 3. Configure the OAuth Consent Screen

1. Go to **APIs & Services → OAuth consent screen**.
2. Select **External** as the user type and click **Create**.
3. Fill in the required fields:
   - **App name:** `delete-old-mails` (or anything you like)
   - **User support email:** your Gmail address
   - **Developer contact email:** your Gmail address
4. Click **Save and Continue** through the Scopes page (no changes needed).
5. On the **Test users** page, click **+ Add Users** and enter your Gmail address (e.g., `yourname@gmail.com`). This is important — without this, you'll get a `403: access_denied` error.
6. Click **Save and Continue**, then **Back to Dashboard**.

### 4. Create OAuth Credentials

1. Go to **APIs & Services → Credentials**.
2. Click **+ Create Credentials → OAuth client ID**.
3. Set **Application type** to **Desktop app**.
4. Name it anything (e.g., `delete-old-mails-client`).
5. Click **Create**.
6. Click **Download JSON** on the popup (or find it in the credentials list and download from there).
7. Rename the downloaded file to `credentials.json` and place it in the project folder alongside `run.py`.

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` contains:

```
google-auth
google-auth-oauthlib
google-api-python-client
```

### 6. Run the Script

```bash
python run.py
```

On the first run, a browser window will open asking you to sign in and authorize the app.

**If you see "Google hasn't verified this app":**

1. Click **Advanced** (bottom-left of the warning page).
2. Click **Go to delete-old-mails (unsafe)**.
3. Click **Allow** to grant Gmail permissions.

This is safe — you wrote the script and it only runs on your machine.

After authorization, a `token.json` file is created so you won't need to authorize again on future runs.

### 7. Watch It Work

The script will print progress as it runs:

```
Deleted 500 emails so far...
Deleted 1000 emails so far...
Deleted 1500 emails so far...
...
All done! Total deleted: 59134
```

## How It Works

- Searches Gmail for all emails matching `older_than:Nm`
- Fetches up to 500 message IDs per API call
- Uses `batchDelete` to permanently delete them (skips Trash entirely)
- Loops until no matching emails remain
- Includes a 1-second delay between batches to respect rate limits

## Customization

To change what gets deleted, edit the `query` variable in `run.py`:

| Query | What it targets |
|-------|----------------|
| `older_than:6m` | Older than 6 months (default) |
| `older_than:1y` | Older than 1 year |
| `older_than:6m -is:starred` | Older than 6 months, but keep starred |
| `older_than:6m from:notifications@example.com` | Only from a specific sender |
| `older_than:6m in:inbox` | Only inbox (not sent, drafts, etc.) |
| `older_than:6m has:attachment` | Only emails with attachments |
| `older_than:6m -label:important` | Skip important-labeled emails |

## Troubleshooting

**`403: access_denied` during authorization**
→ You haven't added yourself as a test user. Go to Cloud Console → APIs & Services → OAuth consent screen → Test users → Add your email.

**`token.json` errors or expired token**
→ Delete `token.json` and run the script again. It will re-authorize.

**`HttpError 429: Rate Limit Exceeded`**
→ Increase the `time.sleep()` value in the script (e.g., from `1` to `3`).

**`HttpError 403: Insufficient Permission`**
→ Delete `token.json` and run again. Make sure you click "Allow" on all permission prompts.

**Script finishes but emails still visible in Gmail**
→ Gmail's UI can take a few minutes to reflect changes. Refresh the page or wait a bit.

## Security Notes

- `credentials.json` contains your OAuth client secret — don't share it publicly.
- `token.json` contains your access token — treat it like a password.
- Add both to `.gitignore` if you're using version control.
- The scope `https://mail.google.com/` grants full Gmail access. Revoke it after use at [Google Account Permissions](https://myaccount.google.com/permissions).

## Cleanup After Use

Once your emails are deleted:

1. Revoke app access at [myaccount.google.com/permissions](https://myaccount.google.com/permissions).
2. Delete `token.json` and `credentials.json` from your machine.
3. Optionally delete the Google Cloud project to clean up completely.