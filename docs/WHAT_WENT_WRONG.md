# What Went Wrong (and What I Learned)

The bot worked. The setup guide was clear. The videos were made and posted. It sold zero copies.

For a long time I assumed that meant nobody wanted it. When I finally went back through the Whop dashboard properly, I found something much dumber.

## Mistake 1: The store was never actually switched on

All four of my products were set to **Hidden**, and all four were marked **"Not listed on Discover."**

Nothing on my store was visible to anyone. Every viewer my YouTube videos sent to whop.com/botdrop landed on a page with no products on it. There was never anything to buy.

I had spent my time on the parts I thought were hard — writing the bot, packaging it, making the videos, connecting a bank account — and never checked the one setting that decided whether any of it was reachable. I assumed that creating a product published it. It doesn't.

**What I learned:** I never verified my own funnel. I never once opened my store the way a stranger would, in a logged-out browser, and tried to get my own product. Five minutes of that in week one would have caught it. Now I test everything from the user's side before I call something launched.

## Mistake 2: Four products for one bot

There wasn't one thing to get, there were four overlapping ones: a "Bot Drop" membership, a free "TeamAvailability," a $9.99 "TeamAvailability," and an $8.99 "Availability Bot."

Even if the store had been visible, a visitor would have had to guess which one they wanted. Confusion is a decision, and the decision is usually to leave.

**What I learned:** make the choice obvious. One product, one price, one button.

## Mistake 3: I made people do the work

To use the bot, someone had to download the source, create their own Discord application, copy a bot token, install Python dependencies, and run a script from a terminal — and keep that terminal open for the bot to stay alive.

Every popular Discord bot works differently: click one link, pick your server, done in ten seconds. I was asking non-developers to do a developer's job before they got any value at all.

**What I learned:** friction kills adoption more effectively than price does. Every step between "I want this" and "this is working" loses people.

## Mistake 4: I charged before anyone had used it

I went straight to a paid listing with no free tier, no trial, and no existing users. Nobody had any evidence the bot worked except my word.

**What I learned:** with no reputation and no users, price isn't the barrier — trust is. Usage has to come first; money can come later.

## Mistake 5: I built first and asked later

I never talked to a single Discord server owner outside my friend group before building. I validated the problem against my own experience and assumed it generalized.

It partly does — coordinating across timezones is a real annoyance — but for most servers the manual alternative (just asking in chat) is good enough.

**What I learned:** "I have this problem" is a hypothesis, not evidence.

## What I got right

- I picked a problem I actually had, so I knew exactly what "working" looked like
- I finished it — a working product, not a half-built prototype
- I learned the whole stack of shipping something: code, packaging, setup docs a non-coder could follow, a storefront, marketing videos, payments
- I went back and found the real cause instead of settling for "I guess nobody wanted it"

## The one-line version

I spent months on the hard parts and lost to a checkbox. Now I test the boring parts first.
