# Bot Drop — Availability Bot (source code)

A Discord bot that collects everyone's available times, converts across timezones, and finds the best overlapping slot for the group.

## Commands

- `/choose_region` — pick your region/timezone from a dropdown
- `/set_availability <times>` — set your free hours (e.g. `Not Available`, `14-16`, `9-12, 18-20`)
- `/show_schedule` — view the server's schedule and the best overlapping time
- `/clear_my_data` — clear your own saved data
- `/help` — in-Discord help

## Setup (running it yourself)

1. **Create a Discord Application**
   - Go to https://discord.com/developers/applications
   - Click **New Application**, give it a name
   - Go to the **Bot** tab, click **Reset Token** (or **Copy** if one exists) to get your bot token — keep this secret

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your bot token**
   - On Windows (PowerShell):
     ```powershell
     setx DISCORD_TOKEN "your-token-here"
     ```
     Then close and reopen PowerShell.
   - On Mac/Linux:
     ```bash
     export DISCORD_TOKEN="your-token-here"
     ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

5. **Invite the bot to your server**
   - Back in the Discord Developer Portal, go to **OAuth2 → URL Generator**
   - Under **Scopes**, check `bot` (and `applications.commands` so slash commands show up)
   - Under **Bot Permissions**, check at least: Send Messages, Embed Links, Use Slash Commands
   - Copy the generated URL, open it in your browser, and pick your server

Keep the process running (locally, or on a host like Railway/Render) for the bot to stay online.
