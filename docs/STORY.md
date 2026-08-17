# The Story

## The problem

In my friend group, we all game together — but we're rarely free at the same time. The frustrating part is that there usually *was* a window where most of us could play; we just never found it. Nobody wanted to be the person messaging six people asking "hey, are you free at 5?", so a lot of good gaming time got wasted because nobody could see the overlap.

## The idea

The summer before 10th grade (May 2025), I decided I wanted to try something ambitious: start a real business on my own, using the one skill I actually had — coding. The fastest way to find out whether my skills held up in the real world was to build something people would pay for.

I had no business experience. I was going into 10th grade. But I picked a problem I understood firsthand — the scheduling mess in my own friend group — and built a Discord bot to fix it: one that takes everyone's free hours, handles the timezone conversion automatically, and tells the group when the most people are actually available.

## Building it

I didn't know how to build a proper Discord bot going in, so I taught myself Python Discord bots from scratch. I tried several AI coding tools and settled on Replit as the one that worked best for me.

The bot does three things: each person picks their region (so it knows their timezone), types in their free hours in plain language, and then the bot calculates the window where the most people overlap — showing the result to everyone in their *own* local time rather than one timezone for the whole group.

Getting the time parsing right was harder than I expected. People type availability in wildly inconsistent ways (`3-4`, `12:30-13:15`, `9:00-12:00, 18:30-20:00`, `Not Available`), and all of it has to become something the program can do math on.

## Turning it into a business

Building the bot was only half of it. I also had to learn to sell it:

- Packaged and listed the bot on **Whop**, a marketplace for digital products
- Set up a **Whop storefront** and a **YouTube channel** ([@Bot-Drop](https://www.youtube.com/@Bot-Drop/shorts)) with short demo videos
- Connected a **bank account** so I could actually get paid

## What happened

It didn't sell. Not one customer.

I could have left it there and called it a failed experiment. Instead I went back and worked out *why*, and the answers were specific and fixable — see [WHAT_WENT_WRONG.md](WHAT_WENT_WRONG.md). The short version: I built a working product and then made it hard to get. Every mistake was on the distribution side, not the code side.

## Where it stands now

I'm fixing the things I got wrong rather than starting over. The bot works; what needs to change is how people get their hands on it. [ROADMAP.md](ROADMAP.md) has the plan.
