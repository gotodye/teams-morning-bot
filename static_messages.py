"""Static B+ message pools — humor, warmth, facts, and novel travel spots.

Humor is workplace/life-general (not engineer-only); facts include Asian trivia;
travel favors off-the-beaten-path places, weighted toward Southeast Asia.
"""

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
        "Monday is just the universe hitting the 'new sprint' button. Stretch first. 🌅",
        "humor",
        mood="humor",
    ),
    _msg(
        "Your Monday to-do list called — it would like to negotiate a shorter contract. 📋",
        "humor",
        mood="humor",
    ),
    _msg(
        "Coffee: Monday's most reliable coworker. ☕",
        "humor",
        mood="coffee",
    ),
    _msg(
        "You're not behind — you're just loading. "
        "Great things take a moment to get going. ⚡",
        "warm",
        mood="warm",
    ),
    _msg(
        "New week, clean slate. Do one thing today you'll be glad about on Friday. 🌱",
        "warm",
        mood="warm",
    ),
    _msg(
        "Honey never spoils — archaeologists found 3,000-year-old honey still edible. "
        "Patience keeps. 🍯",
        "fact",
        mood="nature",
    ),
    _msg(
        "Indonesia spans 17,000+ islands. You don't have to reach them all today — "
        "just set sail for one. 🏝️",
        "fact",
        mood="culture",
    ),
    _msg(
        "Son Doong Cave, Vietnam 🇻🇳\n"
        "The world's largest cave hides its own jungle, river, and clouds underground.\n"
        "Some of the biggest things stay quiet until you go looking.",
        "travel",
        image_query="Son Doong Cave Vietnam largest cave jungle",
    ),
    _msg(
        "Chefchaouen, Morocco 🇲🇦\n"
        "An entire town washed in a hundred shades of blue, tucked into the Rif Mountains.\n"
        "A little color can change the whole mood of a place.",
        "travel",
        image_query="Chefchaouen Morocco blue city streets",
    ),
    _msg(
        "Bagan, Myanmar 🇲🇲\n"
        "Thousands of pagodas rise from morning mist like prayers left standing in gold light.\n"
        "Carry a little of that stillness into your first hour.",
        "travel",
        image_query="Bagan Myanmar temples sunrise balloons",
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
        "'It's just a small change' — famous last words before a very long afternoon. 😅",
        "humor",
        mood="humor",
    ),
    _msg(
        "Your inbox is not a to-do list — it's a suggestion box from the universe. 📥",
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
        "Vietnam is the world's 2nd-largest coffee exporter. "
        "Somewhere, your morning cup is quietly saying cảm ơn. ☕",
        "fact",
        mood="culture",
    ),
    _msg(
        "Hummingbirds are the only birds that can fly backward. "
        "Sometimes reversing course is progress. 🐦",
        "fact",
        mood="nature",
    ),
    _msg(
        "Raja Ampat, Indonesia 🇮🇩\n"
        "Jade islands scatter across glass-clear sea at the edge of the map.\n"
        "The best places rarely sit on the shortest route.",
        "travel",
        image_query="Raja Ampat Indonesia islands aerial turquoise",
    ),
    _msg(
        "Salar de Uyuni, Bolivia 🇧🇴\n"
        "After rain, the salt flats mirror the sky until earth and heaven trade places.\n"
        "Perspective is a place you can visit.",
        "travel",
        image_query="Salar de Uyuni Bolivia salt flats mirror",
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
        "The office plant is thriving on pure neglect. Some of us relate deeply. 🪴",
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
        "Thailand's calendar runs 543 years ahead — over there it's already the 2560s. "
        "You're basically working from the future. 🗓️",
        "fact",
        mood="culture",
    ),
    _msg(
        "Polar bears have black skin under white fur. Don't judge the surface — look deeper. 🐻‍❄️",
        "fact",
        mood="nature",
    ),
    _msg(
        "Kawah Ijen, Indonesia 🇮🇩\n"
        "Electric-blue flames flicker from the crater before dawn — fire the color of the sea.\n"
        "Rare sights reward the early riser.",
        "travel",
        image_query="Kawah Ijen blue fire volcano Indonesia",
    ),
    _msg(
        "Zhangye Danxia, China 🇨🇳\n"
        "Hills striped in red, gold, and turquoise, painted slowly over millions of years.\n"
        "Beauty layered patiently outlasts anything rushed.",
        "travel",
        image_query="Zhangye Danxia rainbow mountains China",
    ),
    _msg(
        "Tiger's Nest, Bhutan 🇧🇹\n"
        "A monastery clings to a cliff above the clouds, reached only on foot.\n"
        "Some heights are meant to be climbed slowly, and on purpose.",
        "travel",
        image_query="Paro Taktsang Tiger's Nest Bhutan monastery",
    ),
]

# --- Thursday: finish-line energy ---
THURSDAY_POOL: list[StaticMessage] = [
    _msg(
        "Thursday energy: not quite Friday, but the trailer looks promising. 🎬",
        "humor",
        mood="humor",
    ),
    _msg(
        "Today's forecast: 80% chance of meetings that could have been an email. ☁️",
        "humor",
        mood="humor",
    ),
    _msg(
        "The office thermostat has three settings: Arctic, Sahara, and 'who touched this'. 🌡️",
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
        "Taipei 101 rides out typhoons on a giant golden pendulum. "
        "Balance under pressure is a design choice. 🏙️",
        "fact",
        mood="architecture",
    ),
    _msg(
        "Sunlight takes 8 minutes 20 seconds to reach Earth. "
        "You're always seeing the past — but building the future. ☀️",
        "fact",
        mood="warm",
    ),
    _msg(
        "Batad Rice Terraces, Philippines 🇵🇭\n"
        "Stone-walled steps climb the mountains like a 2,000-year-old staircase to the clouds.\n"
        "Patience, stacked high enough, becomes a wonder.",
        "travel",
        image_query="Batad rice terraces Philippines amphitheater",
    ),
    _msg(
        "Socotra Island, Yemen 🇾🇪\n"
        "Dragon-blood trees spread like umbrellas on a landscape borrowed from another planet.\n"
        "Strange and rare can still be exactly right.",
        "travel",
        image_query="Socotra Island Yemen dragon blood trees",
    ),
    _msg(
        "Wadi Rum, Jordan 🇯🇴\n"
        "Rose sand and vast silence stretch wider than any to-do list can travel.\n"
        "Step into the morning unhurried.",
        "travel",
        image_query="Wadi Rum Jordan desert red sand",
    ),
]

# --- Friday: light and grateful ---
FRIDAY_POOL: list[StaticMessage] = [
    _msg(
        "Coffee: because adulting requires a loading screen. ☕",
        "humor",
        mood="coffee",
    ),
    _msg(
        "Weekend loading… please keep a little kindness cached for Monday. 💾",
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
        "Kindness is free, remembered, and weirdly contagious. Start a small outbreak today. 💛",
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
        "The world's largest flower, the Rafflesia, blooms in the forests of Sumatra — "
        "rare things are worth the wait. 🌺",
        "fact",
        mood="nature",
    ),
    _msg(
        "Mù Cang Chải, Vietnam 🇻🇳\n"
        "Terraced hillsides ripple gold at harvest, each curve shaped by generations of hands.\n"
        "Steady effort, season after season, carves something beautiful.",
        "travel",
        image_query="Mu Cang Chai Vietnam rice terraces golden",
    ),
    _msg(
        "Lençóis Maranhenses, Brazil 🇧🇷\n"
        "White dunes cradle turquoise lagoons that appear only after the rains.\n"
        "Even a desert keeps a little water for the right moment.",
        "travel",
        image_query="Lencois Maranhenses Brazil dunes lagoons",
    ),
    _msg(
        "Kelimutu, Indonesia 🇮🇩\n"
        "Three crater lakes on one volcano, each a different color — and the colors quietly change.\n"
        "Not everything needs to stay the same to be at peace.",
        "travel",
        image_query="Kelimutu crater lakes Flores Indonesia",
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
        "Micro-challenge: send one colleague a specific thank-you before lunch. "
        "Specific beats generic. 🙏",
        "warm",
        mood="action",
    ),
    _msg(
        "Octopuses have three hearts — which one is keeping yours going this morning? "
        "Reply with what's fueling you. 🐙",
        "fact",
        mood="cute",
    ),
    _msg(
        "Sea otters hold hands while sleeping so they don't drift apart. Teamwork, illustrated. 🦦",
        "fact",
        mood="cute",
    ),
    _msg(
        "Tsingy de Bemaraha, Madagascar 🇲🇬\n"
        "Limestone blades rise into a forest of stone you can only cross by rope and nerve.\n"
        "Some paths are earned, not strolled.",
        "travel",
        image_query="Tsingy de Bemaraha Madagascar stone forest",
    ),
    _msg(
        "Caño Cristales, Colombia 🇨🇴\n"
        "For a few weeks a year, a river blushes red, yellow, and green — the 'liquid rainbow'.\n"
        "Rare timing is its own kind of magic.",
        "travel",
        image_query="Cano Cristales Colombia river of five colors",
    ),
    _msg(
        "Pamukkale, Turkey 🇹🇷\n"
        "White mineral terraces spill down the hillside like frozen waterfalls of milk.\n"
        "Beauty can be built one gentle layer at a time.",
        "travel",
        image_query="Pamukkale Turkey white travertine terraces",
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
