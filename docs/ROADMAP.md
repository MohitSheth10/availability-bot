# Roadmap

Each fix here maps to a mistake in [WHAT_WENT_WRONG.md](WHAT_WENT_WRONG.md). Update the status boxes as things get done.

## 1. Make it free on Whop — *in progress*

Removing the price is the cheapest fix available. The bot has no users and no track record, so charging for it was solving the wrong problem. Free at least lets someone try it.

## 2. Get it hosted and always online — *not started*

The real fix for Mistake 1. One instance of the bot running continuously means users get a single "Add to Discord" link instead of a download and a setup guide. Currently exploring hosting options.

## 3. A proper landing page — *not started*

Once the bot is hosted, a simple page with an "Add to Discord" button (the way Invite Tracker and most established bots do it) becomes the front door, and the Whop listing stops being necessary. Skeleton lives in `website/`.

## 4. List on Discord bot directories — *not started*

Sites like Top.gg and Discord Bot List are where server owners actually go looking for bots. This is the distribution I never built the first time. Only worth doing once the bot is hosted and the one-click invite works.

## 5. Talk to actual server owners — *not started*

Before building anything else, ask people running mid-size Discord servers whether scheduling is a real pain for them and what they'd want it to do. Should have been step one.

## Open questions

- Where does the bot run, and who keeps it running?
- Data currently lives in memory per-server; a hosted version serving many servers will need to persist it somewhere.
