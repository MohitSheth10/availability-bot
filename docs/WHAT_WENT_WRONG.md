# What Went Wrong (and What I Learned)

*(Draft — rewrite the wording in your own voice before this goes public. The substance is right; the phrasing should sound like you.)*

The bot worked. The setup guide was clear. It was listed, priced, and marketed. It still sold zero copies. Here's what I actually got wrong.

## Mistake 1: I made people do the work

To use the bot, a buyer had to download the source code, create their own Discord application, copy a bot token, install Python dependencies, and run a script from a terminal — and keep that terminal open for the bot to stay alive.

Every popular Discord bot works differently: you click one link, pick your server, and it's running in ten seconds. I was asking non-developers to do a developer's job before they got any value at all. Most people would quit at step two.

**What I learned:** friction kills adoption far more effectively than price does. Every step between "I want this" and "this is working" loses people.

## Mistake 2: I charged before anyone had used it

I went straight to a paid listing with no free tier, no trial, and no existing users. Nobody had any evidence the bot worked or was worth paying for except my word.

**What I learned:** with no reputation and no users, price isn't the barrier — trust is. Usage has to come first; money can come later.

## Mistake 3: I built first and asked later

I never talked to a single Discord server owner outside my friend group before building. I validated the problem against my own experience and assumed it generalized.

It partly does — scheduling across timezones is a real annoyance — but for most servers the manual alternative (just asking in chat) is good enough. The problem was real but not painful enough for people to pay to solve.

**What I learned:** "I have this problem" is a hypothesis, not evidence. Talk to ten people before writing code.

## Mistake 4: I marketed to nobody

I made demo videos and posted them to a brand new YouTube channel with no audience, and a Whop listing that nobody had a reason to visit. I built the marketing assets but not the distribution.

**What I learned:** launching to an audience of zero is the same as not launching. Distribution is something you build before you need it, not on launch day.

## What I got right

Worth recording too, since these were real and I'd do them again:

- I picked a problem I actually had, which meant I understood exactly what "working" looked like
- I finished it — a working product, not a half-built prototype
- I learned the full stack of shipping something: code, packaging, setup docs a non-coder could follow, a storefront, marketing videos, and payments
- I went back and diagnosed the failure honestly instead of moving on

## The one-line version

Building the product was the easy half. I learned that a working thing nobody can easily get is worth about the same as a thing that doesn't work.
