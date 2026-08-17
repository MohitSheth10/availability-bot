# Roadmap

Each item maps to a mistake in [WHAT_WENT_WRONG.md](WHAT_WENT_WRONG.md).

## Done

**Turned the store on.** The free product is now actually visible on whop.com/botdrop. This was Mistake 1 — it had been hidden the entire time. *(Aug 2026)*

**Cut four products down to one.** The two paid listings and the overlapping membership product are hidden; there's now a single free "Availability Bot" and nothing else to choose between. This was Mistake 2. *(Aug 2026)*

**Made it free.** No price, no checkout, no reason to hesitate. This was Mistake 4. *(Aug 2026)*

**Wrote a real store page.** The store had no description at all before — just a logo and a name. It now says what the bot does in two sentences. *(Aug 2026)*

## Next

**Get it hosted and always online.** The real fix for Mistake 3. One instance running continuously means users get a single "Add to Discord" link instead of a download and a setup guide. Currently working out where it runs.

**Build a landing page.** Once the bot is hosted, a simple page with an "Add to Discord" button — the way Invite Tracker and most established bots do it — becomes the front door. Skeleton is in `website/`.

**List on Discord bot directories.** Top.gg and Discord Bot List are where server owners actually go looking. This is the distribution I never built the first time. Only worth doing once the one-click invite works.

**Talk to actual server owners.** Ask people running mid-size servers whether scheduling is a real pain and what they'd want. Should have been step one.

## Known issues in the code

See [../bot/README.md](../bot/README.md) for the full list. The two that matter: timezones are fixed offsets, so daylight saving is wrong for about half the year, and nothing is saved to disk, so restarting the bot wipes everyone's availability.

## Open questions

- Where does the bot run, and who keeps it running?
- A hosted version serving many servers needs somewhere to actually store data.
