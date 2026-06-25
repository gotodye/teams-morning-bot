"""Static morning message database — management quotes, philosophy, and card titles."""

from __future__ import annotations

from datetime import date

# Static B+ pools (humor, warm, fact, travel) live in static_messages.py

MANAGEMENT_QUOTES: list[str] = [
    # Verified quotes from renowned leaders, authors, and thinkers
    '💼 Management Moment: "Leadership is not about being in charge. It is about taking care of those in your charge." — Simon Sinek',
    '💼 Management Moment: "Management is doing things right; leadership is doing the right things." — Peter Drucker',
    '💼 Management Moment: "The best way to find out if you can trust somebody is to trust them." — Ernest Hemingway',
    '💼 Management Moment: "It is not the strongest of the species that survives, but the one most adaptable to change." — Charles Darwin',
    '💼 Management Moment: "The function of leadership is to produce more leaders, not more followers." — Ralph Nader',
    '💼 Management Moment: "Done is better than perfect." — Sheryl Sandberg',
    '💼 Management Moment: "Your most unhappy customers are your greatest source of learning." — Bill Gates',
    '💼 Management Moment: "The way to get started is to quit talking and begin doing." — Walt Disney',
    '💼 Management Moment: "Whether you think you can or you think you can\'t, you\'re right." — Henry Ford',
    '💼 Management Moment: "The main thing is to keep the main thing the main thing." — Stephen Covey',
    '💼 Management Moment: "Feedback is the breakfast of champions." — Ken Blanchard',
    '💼 Management Moment: "A leader is one who knows the way, goes the way, and shows the way." — John C. Maxwell',
    '💼 Management Moment: "What gets measured gets managed." — Peter Drucker',
    '💼 Management Moment: "Good is the enemy of great." — Jim Collins',
    '💼 Management Moment: "Culture eats strategy for breakfast." — Peter Drucker',
    '💼 Management Moment: "The secret of getting ahead is getting started." — Mark Twain',
    '💼 Management Moment: "If you want to lift yourself up, lift up someone else." — Booker T. Washington',
    '💼 Management Moment: "No man will make a great leader who wants to do it all himself." — Andrew Carnegie',
    '💼 Management Moment: "Price is what you pay. Value is what you get." — Warren Buffett',
    '💼 Management Moment: "It takes 20 years to build a reputation and five minutes to ruin it." — Warren Buffett',
    '💼 Management Moment: "Success is not final, failure is not fatal: it is the courage to continue that counts." — Winston Churchill',
    '💼 Management Moment: "The only way to do great work is to love what you do." — Steve Jobs',
    '💼 Management Moment: "Great things in business are never done by one person. They\'re done by a team of people." — Steve Jobs',
    '💼 Management Moment: "Innovation distinguishes between a leader and a follower." — Steve Jobs',
    '💼 Management Moment: "The greatest leader is not the one who does the greatest things, but the one who gets people to do the greatest things." — Ronald Reagan',
    '💼 Management Moment: "A genuine leader is not a searcher for consensus but a molder of consensus." — Martin Luther King Jr.',
    '💼 Management Moment: "The art of communication is the language of leadership." — James Humes',
    '💼 Management Moment: "You don\'t build a business. You build people, and then people build the business." — Zig Ziglar',
    '💼 Management Moment: "People will forget what you said, but they will never forget how you made them feel." — Maya Angelou',
]

PHILOSOPHY_QUOTES: list[str] = [
    # Verified quotes from renowned philosophers
    '🪶 Philosophy Moment: "You have power over your mind — not outside events. Realize this, and you will find strength." — Marcus Aurelius',
    '🪶 Philosophy Moment: "We suffer more often in imagination than in reality." — Seneca',
    '🪶 Philosophy Moment: "We are what we repeatedly do. Excellence, then, is not an act, but a habit." — Aristotle',
    '🪶 Philosophy Moment: "The only true wisdom is in knowing you know nothing." — Socrates',
    '🪶 Philosophy Moment: "It does not matter how slowly you go as long as you do not stop." — Confucius',
    '🪶 Philosophy Moment: "It\'s not what happens to you, but how you react to it that matters." — Epictetus',
    '🪶 Philosophy Moment: "He who has a why to live can bear almost any how." — Friedrich Nietzsche',
    '🪶 Philosophy Moment: "The unexamined life is not worth living." — Socrates',
    '🪶 Philosophy Moment: "Happiness is not something ready made. It comes from your own actions." — Dalai Lama',
    '🪶 Philosophy Moment: "The mind is everything. What you think you become." — Buddha',
    '🪶 Philosophy Moment: "Knowing yourself is the beginning of all wisdom." — Aristotle',
    '🪶 Philosophy Moment: "Waste no more time arguing about what a good man should be. Be one." — Marcus Aurelius',
    '🪶 Philosophy Moment: "The only thing I know is that I know nothing." — Socrates',
    '🪶 Philosophy Moment: "Dwell on the beauty of life. Watch the stars, and see yourself running with them." — Marcus Aurelius',
    '🪶 Philosophy Moment: "Life is really simple, but we insist on making it complicated." — Confucius',
    '🪶 Philosophy Moment: "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does." — Jean-Paul Sartre',
    '🪶 Philosophy Moment: "The greatest wealth is to live content with little." — Plato',
    '🪶 Philosophy Moment: "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment." — Ralph Waldo Emerson',
    '🪶 Philosophy Moment: "As is a tale, so is life: not how long it is, but how good it is, is what matters." — Seneca',
    '🪶 Philosophy Moment: "Act only according to that maxim whereby you can at the same time will that it should become a universal law." — Immanuel Kant',
    '🪶 Philosophy Moment: "I think, therefore I am." — René Descartes',
    '🪶 Philosophy Moment: "The journey of a thousand miles begins with a single step." — Laozi',
    '🪶 Philosophy Moment: "No man ever steps in the same river twice, for it\'s not the same river and he\'s not the same man." — Heraclitus',
    '🪶 Philosophy Moment: "Educating the mind without educating the heart is no education at all." — Aristotle',
    '🪶 Philosophy Moment: "Freedom is the only worthy goal in life. It is won by disregarding things that lie beyond our control." — Epictetus',
    '🪶 Philosophy Moment: "The soul becomes dyed with the color of its thoughts." — Marcus Aurelius',
    '🪶 Philosophy Moment: "Wonder is the beginning of wisdom." — Socrates',
    '🪶 Philosophy Moment: "The measure of a man is what he does with power." — Plato',
]

THEME_TITLES: dict[str, str] = {
    "management": "💼 Wisdom from the Greats",
    "article": "📚 This Week's Read",
    "philosophy": "🪶 A Thought to Carry",
    "interaction": "📣 Your Turn — Let's Connect",
    "ai": "✨ Fresh from the Bot Brain",
}

STATIC_TITLES: list[str] = [
    "☀️ Rise & Shine — It's {weekday}",
    "☕ {weekday} Mode: Activated",
    "⚡ {weekday} — Let's Make It Count",
    "🌅 Good Vibes Only — Happy {weekday}",
    "🚀 {weekday} Kickoff",
    "🎯 Focus Mode: {weekday}",
    "✨ {weekday} — Your Main-Character Era",
    "🔥 Bring the Energy — It's {weekday}",
    "💪 {weekday} — You've Got This",
    "🌤️ Morning Boost — {weekday}",
    "📈 Stack Small Wins — {weekday}",
    "🎬 Plot Twist: It's {weekday}",
    "⌨️ {weekday}.exe Is Running Smoothly",
    "☕ Coffee First, Then Conquer {weekday}",
    "🧭 Navigate {weekday} Like a Pro",
    "🌻 {weekday} — Fresh Start, Fresh Mindset",
    "🏃 {weekday} Sprint — Pace Yourself",
    "💡 Curiosity On — Happy {weekday}",
    "🎉 {weekday} — Make Someone's Day",
    "🌈 {weekday} Forecast: 100% Team Spirit",
]

TRAVEL_CARD_TITLES: list[str] = [
    "🌍 A View from Afar",
    "✈️ Morning Postcard from Elsewhere",
    "🗺️ Today's Window to the World",
    "🌅 Travel with Your Eyes",
    "🧳 A Little Escape Before Work",
    "📮 Greetings from Somewhere Beautiful",
]

SUBTITLE_TAGLINES: list[str] = [
    "Small wins stack up",
    "One focused hour beats a scattered day",
    "Show up as your best self",
    "Progress over perfection",
    "Your vibe sets the tone",
    "Make today worth remembering",
    "Start strong, stay kind",
    "You've got more in the tank than you think",
    "Be the colleague you'd want on your team",
    "Curiosity beats certainty",
    "Done with care beats done in a rush",
    "Protect your first 90 minutes",
    "Adapt and advance",
    "Listen for the quiet wins",
    "Energy is a budget — spend wisely",
]

THEME_SUBTITLE_TAGLINES: dict[str, str] = {
    "management": "Leadership · mindset · growth",
    "article": "Read · reflect · apply",
    "philosophy": "Pause · ponder · proceed",
    "interaction": "Share · connect · belong",
    "ai": "Fresh words for a fresh day",
}

TRAVEL_SUBTITLE_TAGLINES: list[str] = [
    "Borrow a moment of elsewhere",
    "Let your eyes wander somewhere beautiful",
    "A quiet trip before the first meeting",
    "Somewhere far, feeling near",
    "Travel light — even if only in your mind",
]


def _pick_by_date(pool: list[str], today: date) -> str:
    return pool[today.toordinal() % len(pool)]


def build_card_title(
    today: date,
    source: str,
    weekday_name: str,
    *,
    static_format: str | None = None,
) -> str:
    """Build Adaptive Card title — theme-specific or rotating static pool."""
    if source in THEME_TITLES:
        return THEME_TITLES[source]
    if static_format == "travel":
        return _pick_by_date(TRAVEL_CARD_TITLES, today)
    template = _pick_by_date(STATIC_TITLES, today)
    return template.replace("{weekday}", weekday_name)


def build_card_subtitle(
    today: date,
    source: str,
    weekday_name: str,
    *,
    static_format: str | None = None,
) -> str:
    """Date line with an optional short tagline."""
    date_str = today.strftime("%B %d, %Y")
    if source in THEME_SUBTITLE_TAGLINES:
        tagline = THEME_SUBTITLE_TAGLINES[source]
    elif static_format == "travel":
        tagline = _pick_by_date(TRAVEL_SUBTITLE_TAGLINES, today)
    else:
        tagline = _pick_by_date(SUBTITLE_TAGLINES, today)
    return f"{weekday_name}, {date_str} · {tagline}"
