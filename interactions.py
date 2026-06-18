"""Biweekly channel interaction prompts — mostly reply-in-thread, occasionally Forms."""

from __future__ import annotations

from datetime import date
from typing import Literal, TypedDict


class Interaction(TypedDict):
    headline: str
    body: str
    kind: Literal["channel", "forms"]
    channel_fallback: str


INTERACTIONS: list[Interaction] = [
    # Growth — channel
    {
        "headline": "Small Wins",
        "kind": "channel",
        "body": (
            "What's one small win from the past two weeks — at work or in life? "
            "It can be tiny: a habit kept, a problem solved, or a moment you're proud of."
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Lesson Learned",
        "kind": "channel",
        "body": (
            "What's one thing you learned in the last two weeks that changed how you work "
            "or how you show up for others?"
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Gratitude Shout-out",
        "kind": "channel",
        "body": (
            "Shout-out time! Name one colleague who made your last two weeks easier, "
            "smarter, or more fun — and tell us what they did."
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Energy Check",
        "kind": "channel",
        "body": (
            "Honest check-in: what gave you energy at work recently, and what drained it? "
            "Sharing patterns helps us all work smarter together."
        ),
        "channel_fallback": "",
    },
    # Fun — channel
    {
        "headline": "This or That?",
        "kind": "channel",
        "body": (
            "Quick vote — reply with **A** or **B**:\n"
            "**A)** Deep-focus morning (quiet, solo, heads-down)\n"
            "**B)** Collaborative morning (syncs, chats, pair work)\n"
            "No wrong answers — just curious what the channel prefers!"
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Finish This Sentence",
        "kind": "channel",
        "body": (
            'Complete this in one line: **"The best part of a workday morning is ___"**\n'
            "Funniest or most honest reply wins bragging rights. 😄"
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Desk / WFH View",
        "kind": "channel",
        "body": (
            "Show us your morning vibe! Reply with one emoji that describes your desk "
            "or WFH setup today — or tell us what drink is powering your morning. ☕🍵"
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Two Truths & a Lie",
        "kind": "channel",
        "body": (
            "Play along: share **two true facts** and **one lie** about yourself "
            "(work-friendly!). Others can guess which is the lie in the replies."
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Weekend Preview",
        "kind": "channel",
        "body": (
            "It's been two weeks — what's one thing you're looking forward to this weekend, "
            "big or small? Bonus points for creative answers."
        ),
        "channel_fallback": "",
    },
    # Growth + fun blend
    {
        "headline": "Advice to Past You",
        "kind": "channel",
        "body": (
            "If you could tell yourself something two weeks ago, what would it be? "
            "Work tip, mindset shift, or life hack — all welcome."
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Skill Spotlight",
        "kind": "channel",
        "body": (
            "What's one skill — technical or soft — you've been building lately? "
            "Share what you're practicing and why it matters to you."
        ),
        "channel_fallback": "",
    },
    {
        "headline": "Team Superpower",
        "kind": "channel",
        "body": (
            "In one sentence: what do you think this team's superpower is? "
            "Let's see if we describe ourselves the same way."
        ),
        "channel_fallback": "",
    },
    # Forms — occasional pulse checks (~1 in 4 biweeks when URL is set)
    {
        "headline": "Biweekly Pulse Check",
        "kind": "forms",
        "body": (
            "Time for a quick team pulse! Your input helps us understand how work is "
            "feeling — workload, focus, collaboration, and morale."
        ),
        "channel_fallback": (
            "How are the last two weeks treating you — workload, focus, and team vibe? "
            "Reply with one word or a short sentence. All honest answers welcome."
        ),
    },
    {
        "headline": "Growth Reflection",
        "kind": "forms",
        "body": (
            "Biweekly reflection: what's one habit or mindset that's helping you grow "
            "right now — and one you'd like to improve?"
        ),
        "channel_fallback": (
            "What's one habit that's helping you grow right now, and one you'd like "
            "to improve? Reply in the thread — no pressure, just reflection."
        ),
    },
    {
        "headline": "Ways of Working",
        "kind": "forms",
        "body": (
            "We're checking in on how we collaborate. What should we start, stop, "
            "or keep doing as a team over the next two weeks?"
        ),
        "channel_fallback": (
            "What should we **start**, **stop**, or **keep** doing as a team? "
            "Reply with one idea — Start/Stop/Keep format optional but fun."
        ),
    },
    {
        "headline": "Wellbeing Snapshot",
        "kind": "forms",
        "body": (
            "A quick wellbeing snapshot: how balanced do you feel between work and "
            "recovery these days? Your perspective matters."
        ),
        "channel_fallback": (
            "On a scale of 1–5, how balanced do you feel between work and recovery "
            "lately? Reply with your number and optional context."
        ),
    },
]


def pick_interaction(today: date) -> Interaction:
    """Pick one interaction prompt per biweek (deterministic rotation)."""
    year, week, _ = today.isocalendar()
    biweek = (week - 1) // 2
    index = (year * 100 + biweek) % len(INTERACTIONS)
    return INTERACTIONS[index]
