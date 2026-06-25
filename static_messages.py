"""Static B+ message pools — humor, warmth, facts, and literary travel spots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal, NotRequired, TypedDict

StaticFormat = Literal["humor", "warm", "fact", "travel"]


class StaticMessage(TypedDict):
    text: str
    format: StaticFormat
    mood: NotRequired[str]
    image_query: NotRequired[str]


@dataclass(frozen=True)
class StaticPick:
    text: str
    static_format: str
    mood: str | None = None
    image_query: str | None = None


def _msg(
    text: str,
    fmt: StaticFormat,
    *,
    mood: str = "",
    image_query: str = "",
) -> StaticMessage:
    entry: StaticMessage = {"text": text, "format": fmt}
    if mood:
        entry["mood"] = mood
    if image_query:
        entry["image_query"] = image_query
    return entry


# --- Monday: kickoff energy ---
MONDAY_POOL: list[StaticMessage] = [
    _msg(
        "Your brain before coffee is like legacy code — it works, "
        "but nobody should touch it before 9 AM. ☕",
        "humor",
        mood="humor",
    ),
    _msg(
        "Monday has a PR problem. Good thing we're here to rewrite the narrative. 📝",
        "humor",
        mood="humor",
    ),
    _msg(
        "Why do programmers prefer dark mode? Because light attracts bugs. 🐛",
        "humor",
        mood="humor",
    ),
    _msg(
        "You're not behind — you're just loading. "
        "Great things take a moment to initialize. ⚡",
        "warm",
        mood="warm",
    ),
    _msg(
        "New week, clean branch. Commit something you'll be proud of by Friday. 🌅",
        "warm",
        mood="warm",
    ),
    _msg(
        "Honey never spoils — archaeologists found 3,000-year-old honey still edible. "
        "Patience has its rewards. 🍯",
        "fact",
        mood="nature",
    ),
    _msg(
        "Octopuses have three hearts. You only need one — fill it with purpose today. 🐙",
        "fact",
        mood="cute",
    ),
    _msg(
        "Santorini, Greece 🇬🇷\n"
        "White walls hold the morning light like unfinished poems.\n"
        "The Aegean doesn't hurry — and for a moment, neither should we.",
        "travel",
        image_query="Santorini Greece blue domes caldera sunrise landscape",
    ),
    _msg(
        "Ha Long Bay, Vietnam 🇻🇳\n"
        "Limestone islands drift on mist like thoughts surfacing slowly from deep water.\n"
        "Some mornings are meant to be looked at, not solved.",
        "travel",
        image_query="Ha Long Bay Vietnam limestone karst mist scenic",
    ),
    _msg(
        "Arashiyama, Kyoto 🇯🇵\n"
        "Bamboo shadows sway in a green half-light, as if time folded itself quieter here.\n"
        "Carry a little of that stillness into your first hour.",
        "travel",
        image_query="Arashiyama bamboo grove Kyoto Japan morning light",
    ),
]

# --- Tuesday: steady momentum ---
TUESDAY_POOL: list[StaticMessage] = [
    _msg(
        "Meetings: where minutes are kept and hours are lost. "
        "Let's break the trend today. ⏰",
        "humor",
        mood="humor",
    ),
    _msg(
        "'It's just a small change' — famous last words before a two-week sprint. 😅",
        "humor",
        mood="humor",
    ),
    _msg(
        "Ctrl+Z works in code, not in meetings. Think before you speak. ⌨️",
        "humor",
        mood="humor",
    ),
    _msg(
        "Monday didn't break you. That's not luck — that's capability. Keep rolling. 💪",
        "warm",
        mood="warm",
    ),
    _msg(
        "Treat your energy like a budget — spend it on what actually moves the needle. 💡",
        "warm",
        mood="warm",
    ),
    _msg(
        "Small wins compound like interest. Stack one before lunch. 📈",
        "warm",
        mood="warm",
    ),
    _msg(
        "Bananas are berries, but strawberries aren't. Nature loves plot twists — so should we. 🍌",
        "fact",
        mood="nature",
    ),
    _msg(
        "Hummingbirds are the only birds that can fly backward. "
        "Sometimes reversing course is progress. 🐦",
        "fact",
        mood="nature",
    ),
    _msg(
        "Lake Louise, Canada 🇨🇦\n"
        "Turquoise water mirrors pine and snow like the earth is dreaming in color.\n"
        "Let a little of that clarity settle in before the inbox opens.",
        "travel",
        image_query="Lake Louise Banff Canada turquoise lake mountains scenic",
    ),
    _msg(
        "Machu Picchu, Peru 🇵🇪\n"
        "Clouds wander through ancient stone as if memory itself were breathing.\n"
        "Some heights are reached slowly — and beautifully.",
        "travel",
        image_query="Machu Picchu Peru clouds ancient ruins landscape",
    ),
]

# --- Wednesday: midweek lift (backup when not management day) ---
WEDNESDAY_POOL: list[StaticMessage] = [
    _msg(
        "The coffee isn't ready until the first 'quick sync' of the day is survived. ☕",
        "humor",
        mood="coffee",
    ),
    _msg(
        "Debugging is like being a detective in a crime movie where you're also the murderer. 🔍",
        "humor",
        mood="humor",
    ),
    _msg(
        "My code doesn't have bugs — it has undocumented features. (Kidding. Mostly.) 🙃",
        "humor",
        mood="humor",
    ),
    _msg(
        "Halfway up the mountain — the view from here is already worth it. Keep climbing. ⛰️",
        "warm",
        mood="warm",
    ),
    _msg(
        "Done is better than perfect — but 'done with care' is better than both. ✨",
        "warm",
        mood="warm",
    ),
    _msg(
        "Polar bears have black skin under white fur. Don't judge the surface — look deeper. 🐻‍❄️",
        "fact",
        mood="nature",
    ),
    _msg(
        "Water is densest at 4°C — that's why ice floats. Stay flexible; rigidity sinks. 💧",
        "fact",
        mood="nature",
    ),
    _msg(
        "Mount Fuji, Japan 🇯🇵\n"
        "Snow-capped peak above a sea of clouds — quiet, vast, and impossibly still.\n"
        "Clarity often arrives before the noise of the day.",
        "travel",
        image_query="Mount Fuji sunrise clouds Japan landscape scenic",
    ),
    _msg(
        "Blue Lagoon, Iceland 🇮🇸\n"
        "Steam rises from milky blue water under a pale Nordic sky — earth breathing softly.\n"
        "Let today begin a little softer than yesterday.",
        "travel",
        image_query="Blue Lagoon Iceland geothermal steam scenic landscape",
    ),
    _msg(
        "Amalfi Coast, Italy 🇮🇹\n"
        "Cliffs spill into cobalt water as if the coastline were painted in one confident stroke.\n"
        "Beauty, sometimes, is simply paying attention.",
        "travel",
        image_query="Amalfi Coast Italy cliff sea colorful village scenic",
    ),
]

# --- Thursday: finish-line energy ---
THURSDAY_POOL: list[StaticMessage] = [
    _msg(
        "'Works on my machine' is not a deployment strategy. Let's ship with confidence. 🚀",
        "humor",
        mood="humor",
    ),
    _msg(
        "Today's energy: 60% coffee, 30% curiosity, 10% controlled chaos. Blend well. ☕",
        "humor",
        mood="coffee",
    ),
    _msg(
        "A clean desk is a sign of a cluttered hard drive. Organize priorities, not just icons. 🖥️",
        "humor",
        mood="humor",
    ),
    _msg(
        "The weekend is waving from the horizon. Finish strong, not rushed. 🌅",
        "warm",
        mood="warm",
    ),
    _msg(
        "Protect your first 90 minutes — they're the quiet architects of the whole day. 🎯",
        "warm",
        mood="warm",
    ),
    _msg(
        "Sunlight takes 8 minutes 20 seconds to reach Earth. "
        "You're always seeing the past — but building the future. ☀️",
        "fact",
        mood="warm",
    ),
    _msg(
        "The Eiffel Tower grows ~15 cm taller in summer. Expand your comfort zone today. 🗼",
        "fact",
        mood="nature",
    ),
    _msg(
        "Geirangerfjord, Norway 🇳🇴\n"
        "Waterfalls thread down green cliffs into still fjord water — nature in no hurry at all.\n"
        "Borrow that unhurried grace for the hours ahead.",
        "travel",
        image_query="Geirangerfjord Norway fjord waterfall scenic landscape",
    ),
    _msg(
        "Cappadocia, Turkey 🇹🇷\n"
        "Balloons drift over honey-colored valleys at dawn, as if the sky were gently exhaling.\n"
        "Lift your mood before the day asks you to.",
        "travel",
        image_query="Cappadocia Turkey hot air balloons sunrise valley",
    ),
    _msg(
        "Maldives 🇲🇻\n"
        "Sand so pale and water so clear the horizon forgets where one ends and the other begins.\n"
        "Float through this morning, even if only in your imagination.",
        "travel",
        image_query="Maldives turquoise lagoon overwater villa scenic aerial",
    ),
]

# --- Friday: light and grateful ---
FRIDAY_POOL: list[StaticMessage] = [
    _msg(
        "Why did the developer go broke? Because they used up all their cache. Ba dum tss. 💸",
        "humor",
        mood="humor",
    ),
    _msg(
        "Pro tip: the reply-all button is a group trust exercise. Choose wisely. 📧",
        "humor",
        mood="humor",
    ),
    _msg(
        "Stand-up meetings are cardio for your career. Show up, speak up, level up. 🏃",
        "humor",
        mood="humor",
    ),
    _msg(
        "TGIF — you earned this week. Close loops, celebrate wins, recharge well. 🎉",
        "warm",
        mood="warm",
    ),
    _msg(
        "You can't pour from an empty cup. Fill yours first — then serve the team. 🫖",
        "warm",
        mood="warm",
    ),
    _msg(
        "Penguins give pebbles as gifts to show affection. "
        "Who on your team deserves a quiet thank-you today? 🐧",
        "fact",
        mood="cute",
    ),
    _msg(
        "Cows have best friends and get stressed when separated. "
        "Check in on your work buddy before the week ends. 🐄",
        "fact",
        mood="cute",
    ),
    _msg(
        "Santorini at dusk, Greece 🇬🇷\n"
        "Gold light pools in narrow streets as the sea turns violet — evening arriving like a slow compliment.\n"
        "Close the week with something gentle.",
        "travel",
        image_query="Santorini Greece sunset golden hour caldera scenic",
    ),
    _msg(
        "Milford Sound, New Zealand 🇳🇿\n"
        "Rain-misted peaks rise from dark water like the world is whispering in lowercase.\n"
        "Take one quiet breath before the week lets go.",
        "travel",
        image_query="Milford Sound New Zealand fjord mountains mist scenic",
    ),
    _msg(
        "Lavender fields, Provence 🇫🇷\n"
        "Purple rows breathe fragrance into warm air — summer holding still for one last look.\n"
        "End the week colorfully, even if only in your mind.",
        "travel",
        image_query="Provence France lavender fields summer scenic landscape",
    ),
]

STATIC_GENERAL: list[StaticMessage] = [
    _msg(
        "Plot twist: you're the main character today. Act accordingly. 🎬",
        "humor",
        mood="humor",
    ),
    _msg(
        "If Plan A fails, remember: the alphabet has 25 more letters. Adapt and advance. 🔤",
        "humor",
        mood="humor",
    ),
    _msg(
        "Be the colleague you'd want to sit next to in a three-hour meeting. 😄",
        "warm",
        mood="warm",
    ),
    _msg(
        "Progress whispers before it shouts. Listen for the small wins today. 👂",
        "warm",
        mood="warm",
    ),
    _msg(
        "You are about 1 cm taller in the morning. Stand tall in every sense today. 📏",
        "fact",
        mood="nature",
    ),
    _msg(
        "A snail can sleep for three years. Friday mood? We feel you. But we're awake now. 😄",
        "fact",
        mood="cute",
    ),
    _msg(
        "Petra, Jordan 🇯🇴\n"
        "Rose-red stone glows in narrow canyon light — a city half memory, half miracle.\n"
        "Wonder is never wasted on a workday morning.",
        "travel",
        image_query="Petra Jordan Treasury rose red canyon scenic",
    ),
    _msg(
        "Grand Canyon, USA 🇺🇸\n"
        "Layers of time exposed in copper and rust — the earth telling stories without words.\n"
        "Step into today knowing some depths are worth admiring.",
        "travel",
        image_query="Grand Canyon USA sunrise scenic landscape aerial",
    ),
    _msg(
        "Bora Bora, French Polynesia 🇵🇫\n"
        "Lagoon blue so vivid it feels borrowed from a dream you almost remember.\n"
        "Let your shoulders drop — the weekend is nearer than it looks.",
        "travel",
        image_query="Bora Bora turquoise lagoon overwater bungalow scenic",
    ),
    _msg(
        "Serengeti at dawn, Tanzania 🇹🇿\n"
        "Golden grass holds the first light as the plain wakes in slow, ancient rhythm.\n"
        "Begin today with that same unhurried courage.",
        "travel",
        image_query="Serengeti Tanzania savanna sunrise golden landscape wildlife",
    ),
]

STATIC_BY_WEEKDAY: dict[int, list[StaticMessage]] = {
    0: MONDAY_POOL,
    1: TUESDAY_POOL,
    2: WEDNESDAY_POOL,
    3: THURSDAY_POOL,
    4: FRIDAY_POOL,
}


def _pool_for(today: date) -> list[StaticMessage]:
    if today.weekday() in STATIC_BY_WEEKDAY:
        return STATIC_BY_WEEKDAY[today.weekday()]
    return STATIC_GENERAL


def pick_static_message(today: date) -> StaticPick:
    """Pick static B+ message via half-year content batch."""
    from content_batch import pick_static

    return pick_static(today)
