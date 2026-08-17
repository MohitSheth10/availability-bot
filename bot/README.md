# Bot Drop — Availability Bot (source code)

A Discord bot that collects everyone's available times, converts across timezones, and finds the best overlapping slot for the group.

## Commands

- `/choose_region` — pick your region/timezone from a dropdown
- `/set_availability <times>` — set your free hours (e.g. `Not Available`, `14-16`, `9-12, 18-20`)
- `/show_schedule` — view the server's schedule and the best overlapping time
- `/clear_my_data` — clear your own saved data
- `/help` — in-Discord help

## How the matching works

Each person's local hours are converted to UTC using their region's offset, then chopped into 15-minute blocks. The bot counts how many people are free in each block, merges neighboring blocks that have the same people, keeps any run of at least 30 minutes, and sorts by headcount. Results are converted back into each person's own local time before being shown.

## Setup

1. **Create a Discord Application**
   - Go to https://discord.com/developers/applications
   - Click **New Application**, give it a name
   - Go to the **Bot** tab and copy the token — keep this secret, it's the bot's password

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your bot token**
   - Windows (PowerShell):
     ```powershell
     setx DISCORD_TOKEN "your-token-here"
     ```
     Then close and reopen PowerShell.
   - Mac/Linux:
     ```bash
     export DISCORD_TOKEN="your-token-here"
     ```

   See `.env.example` for the full list of settings.

4. **Run the bot**
   ```bash
   python bot.py
   ```

5. **Invite the bot to your server**
   - In the Developer Portal, go to **OAuth2 → URL Generator**
   - Scopes: check `bot` and `applications.commands`
   - Bot Permissions: Send Messages, Embed Links
   - Open the generated URL and pick your server

The bot only runs while the process is running. Close the terminal and it goes offline.

## Known limitations

These are real and worth knowing before you rely on it:

- **No daylight saving handling.** Regions are mapped to fixed UTC offsets in `config.py`, so for roughly half the year the times are off by an hour for anywhere that observes DST. Fixing this properly means using real timezone names (`zoneinfo`) instead of fixed numbers.
- **Nothing is saved to disk.** All availability lives in memory, so restarting the bot wipes every server's data and everyone has to re-enter their times.
- **Regions, not timezones.** You pick from ten broad regions rather than your actual timezone, so anyone whose country doesn't match the offset picked for their region gets the wrong answer.
- **One schedule per server, no dates.** Availability is a daily pattern with no concept of "Tuesday" or a specific date, and there's only one shared schedule per server.
- **No permission checks.** Any member can run any command.
