"""Static morning message database — management quotes, philosophy, and card titles."""

from __future__ import annotations

from datetime import date

# Static B+ pools (humor, warm, fact, travel) live in static_messages.py

MANAGEMENT_QUOTES: list[str] = [
    # Verified quotes from renowned leaders, authors, and thinkers (~80:20 global:Asian)
    '💼 Management Moment: "Leadership is not about being in charge. It is about taking care of those in your charge." — Simon Sinek',
    '💼 Management Moment: "Management is doing things right; leadership is doing the right things." — Peter Drucker',
    '💼 Management Moment: "The best way to find out if you can trust somebody is to trust them." — Ernest Hemingway',
    '💼 Management Moment: "It is not the strongest of the species that survives, but the one most adaptable to change." — Charles Darwin',
    '💼 Management Moment: "I don\'t believe in taking right decisions. I take decisions and then make them right." — Ratan Tata',
    '💼 Management Moment: "Done is better than perfect." — Sheryl Sandberg',
    '💼 Management Moment: "Your most unhappy customers are your greatest source of learning." — Bill Gates',
    '💼 Management Moment: "The way to get started is to quit talking and begin doing." — Walt Disney',
    '💼 Management Moment: "Whether you think you can or you think you can\'t, you\'re right." — Henry Ford',
    '💼 Management Moment: "The main thing is to keep the main thing the main thing." — Stephen Covey',
    '💼 Management Moment: "Feedback is the breakfast of champions." — Ken Blanchard',
    '💼 Management Moment: "A leader is one who knows the way, goes the way, and shows the way." — John C. Maxwell',
    '💼 Management Moment: "Love your job, but never fall in love with your company — because you never know when the company stops loving you." — N. R. Narayana Murthy',
    '💼 Management Moment: "Good is the enemy of great." — Jim Collins',
    '💼 Management Moment: "Culture eats strategy for breakfast." — Peter Drucker',
    '💼 Management Moment: "The secret of getting ahead is getting started." — Mark Twain',
    '💼 Management Moment: "If you want to lift yourself up, lift up someone else." — Booker T. Washington',
    '💼 Management Moment: "No man will make a great leader who wants to do it all himself." — Andrew Carnegie',
    '💼 Management Moment: "The mission of a business is to contribute to the progress and welfare of society." — Konosuke Matsushita',
    '💼 Management Moment: "Price is what you pay. Value is what you get." — Warren Buffett',
    '💼 Management Moment: "In every decision, ask yourself what is the right thing to do as a human being." — Kazuo Inamori',
    '💼 Management Moment: "Success is not final, failure is not fatal: it is the courage to continue that counts." — Winston Churchill',
    '💼 Management Moment: "In the midst of chaos, there is also opportunity." — Sun Tzu',
    '💼 Management Moment: "Innovation distinguishes between a leader and a follower." — Steve Jobs',
    '💼 Management Moment: "The only way to do great work is to love what you do." — Steve Jobs',
    '💼 Management Moment: "A genuine leader is not a searcher for consensus but a molder of consensus." — Martin Luther King Jr.',
    '💼 Management Moment: "Leadership is hard to define, and good leadership even harder. But if you can get people to follow you to the ends of the earth, you are a great leader." — Indra Nooyi',
    '💼 Management Moment: "You don\'t build a business. You build people, and then people build the business." — Zig Ziglar',
    '💼 Management Moment: "People will forget what you said, but they will never forget how you made them feel." — Maya Angelou',
]

PHILOSOPHY_QUOTES: list[str] = [
    # Verified quotes from renowned philosophers, plus Southeast Asian proverbs
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
    '🪶 Philosophy Moment: "Grind iron with enough patience, and one day it becomes a needle." — Vietnamese proverb',
    '🪶 Philosophy Moment: "Dwell on the beauty of life. Watch the stars, and see yourself running with them." — Marcus Aurelius',
    '🪶 Philosophy Moment: "Life is really simple, but we insist on making it complicated." — Confucius',
    '🪶 Philosophy Moment: "Little by little, over time it becomes a hill." — Indonesian proverb',
    '🪶 Philosophy Moment: "The greatest wealth is to live content with little." — Plato',
    '🪶 Philosophy Moment: "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment." — Ralph Waldo Emerson',
    '🪶 Philosophy Moment: "As is a tale, so is life: not how long it is, but how good it is, is what matters." — Seneca',
    '🪶 Philosophy Moment: "Go slowly, and you will get a beautiful blade." — Thai proverb',
    '🪶 Philosophy Moment: "I think, therefore I am." — René Descartes',
    '🪶 Philosophy Moment: "The journey of a thousand miles begins with a single step." — Laozi',
    '🪶 Philosophy Moment: "No man ever steps in the same river twice, for it\'s not the same river and he\'s not the same man." — Heraclitus',
    '🪶 Philosophy Moment: "Educating the mind without educating the heart is no education at all." — Aristotle',
    '🪶 Philosophy Moment: "Freedom is the only worthy goal in life. It is won by disregarding things that lie beyond our control." — Epictetus',
    '🪶 Philosophy Moment: "The soul becomes dyed with the color of its thoughts." — Marcus Aurelius',
    '🪶 Philosophy Moment: "Wonder is the beginning of wisdom." — Socrates',
    '🪶 Philosophy Moment: "The measure of a man is what he does with power." — Plato',
]

TECH_TIDBITS: list[str] = [
    # Bilingual (EN + 中文) curated tech knowledge — weekly "科技新知" slot
    "💡 Tech Tidbit · 科技新知\nThe word \"robot\" comes from the Czech \"robota\" (forced labor), coined in a 1920 play — decades before real robots existed.\n機器人「robot」源自捷克語 robota(強迫勞動),1920 年的舞台劇就先造了這個字,比真正的機器人早了數十年。",
    "💡 Tech Tidbit · 科技新知\nThe first computer \"bug\" was a real moth, found stuck in a Harvard relay in 1947 and taped into the logbook.\n史上第一個電腦「bug」是真的蟲:1947 年一隻飛蛾卡在哈佛的繼電器裡,被貼進了紀錄本。",
    "💡 Tech Tidbit · 科技新知\n\"Wi-Fi\" doesn't actually stand for anything — it's just a catchy brand name, not \"Wireless Fidelity.\"\nWi-Fi 其實不是任何縮寫,只是個好記的品牌名,並非「Wireless Fidelity」。",
    "💡 Tech Tidbit · 科技新知\nThere are more possible games of chess than atoms in the observable universe — which is why AI can't just brute-force it.\n西洋棋可能的棋局比可觀測宇宙的原子還多,所以 AI 無法靠窮舉取勝。",
    "💡 Tech Tidbit · 科技新知\nAn average smartphone today has far more computing power than all of NASA had when it sent humans to the Moon in 1969.\n今天一支普通手機的運算力,遠超過 1969 年 NASA 送人類登月時的全部電腦。",
    "💡 Tech Tidbit · 科技新知\n\"Bluetooth\" is named after a 10th-century Danish king who united tribes — the logo merges his initials in runes.\n藍牙(Bluetooth)以 10 世紀統一部族的丹麥國王命名,logo 是他姓名縮寫的古北歐符文合體。",
    "💡 Tech Tidbit · 科技新知\nQWERTY keyboards were designed in the 1870s partly to slow typists down, so mechanical typewriter arms wouldn't jam.\nQWERTY 鍵盤是 1870 年代設計的,部分目的竟是「放慢」打字速度,以免打字機的連桿卡住。",
    "💡 Tech Tidbit · 科技新知\nThe entire early internet — ARPANET in 1969 — connected just four computers.\n整個早期網際網路(1969 年的 ARPANET)當時只連接了 4 台電腦。",
    "💡 Tech Tidbit · 科技新知\n\"Spam\" email is named after a Monty Python sketch where the word is repeated endlessly — just like junk mail.\n垃圾郵件叫「spam」,典故來自 Monty Python 把這個字講個不停的短劇,就像灌不完的廣告信。",
    "💡 Tech Tidbit · 科技新知\nThe @ symbol was nearly forgotten until 1971, when an engineer picked it to separate user from host in the first email.\n@ 符號曾幾乎被遺忘,直到 1971 年一位工程師選它來分隔使用者與主機,寫出第一封 email。",
    "💡 Tech Tidbit · 科技新知\nMost of the world's internet traffic travels through undersea cables laid across the ocean floor — not satellites.\n全球大部分網路流量其實走海底電纜,而非衛星,一條條鋪在大洋底部。",
    "💡 Tech Tidbit · 科技新知\nThe first 1 GB hard drive (IBM, 1980) weighed about 250 kg and cost $40,000. A tiny chip now holds thousands of times more.\n第一顆 1GB 硬碟(IBM,1980)重約 250 公斤、要價 4 萬美元;如今一枚小晶片的容量是它的數千倍。",
    "💡 Tech Tidbit · 科技新知\n\"Debugging\" predates computers — Thomas Edison used \"bugs\" to describe technical faults back in the 1870s.\n「除錯(debug)」比電腦還早:1870 年代愛迪生就用「bug」來形容技術故障。",
    "💡 Tech Tidbit · 科技新知\nA 12-character random password can take centuries to crack by brute force — adding length beats adding symbols.\n一組 12 個隨機字元的密碼,暴力破解可能要數百年;增加「長度」比加符號更有效。",
    "💡 Tech Tidbit · 科技新知\nThe cloud is just someone else's computer — your data physically lives in a warehouse full of servers somewhere.\n所謂「雲端」其實是別人的電腦:你的資料實際存在某處一整棟塞滿伺服器的機房裡。",
    "💡 Tech Tidbit · 科技新知\nGPS satellites must correct for Einstein's relativity — their clocks tick faster in orbit, or maps would drift kilometres a day.\nGPS 衛星必須校正愛因斯坦的相對論效應:軌道上的時鐘走得較快,否則定位每天會漂移數公里。",
    "💡 Tech Tidbit · 科技新知\nThe first webcam (Cambridge, 1991) was invented just to watch a coffee pot, so people wouldn't walk to an empty one.\n第一台網路攝影機(劍橋,1991)發明的唯一目的,是盯著咖啡壺,免得大家白跑一趟。",
    "💡 Tech Tidbit · 科技新知\nEmoji means \"picture character\" in Japanese (絵文字) — its resemblance to \"emotion\" is a happy coincidence.\nEmoji 在日文是「絵文字」(圖畫文字),和英文 emotion 的相似純屬巧合。",
    "💡 Tech Tidbit · 科技新知\nMoore's Law — chips roughly doubling in power every two years — held for about 50 years and reshaped the modern world.\n摩爾定律(晶片效能約每兩年翻倍)維持了近 50 年,徹底重塑了現代世界。",
    "💡 Tech Tidbit · 科技新知\nHumanity now generates more data every couple of days than it created in total up to the year 2003.\n如今人類每隔幾天產生的資料量,就超過 2003 年以前歷史上累積的總和。",
    "💡 Tech Tidbit · 科技新知\nA modern electric car runs on more lines of software code than a fighter jet or the Space Shuttle did.\n一輛現代電動車搭載的程式碼行數,比一架戰鬥機、甚至當年的太空梭還多。",
    "💡 Tech Tidbit · 科技新知\nTraining a large AI model can involve trillions of words — more text than a person could read in many lifetimes.\n訓練一個大型 AI 模型可能用到數兆個字,比一個人好幾輩子能讀的還多。",
    "💡 Tech Tidbit · 科技新知\nThe first message sent over the internet in 1969 was meant to be \"LOGIN\" — the system crashed after just \"LO.\"\n1969 年第一則網路訊息本想傳「LOGIN」,系統送到「LO」就當機了。",
    "💡 Tech Tidbit · 科技新知\nA single modern GPU can do more calculations per second than the fastest supercomputer on Earth did in the year 2000.\n一張現代 GPU 每秒的運算量,已超過 2000 年全世界最快的超級電腦。",
]

THEME_TITLES: dict[str, str] = {
    "management": "💼 Wisdom from the Greats",
    "article": "📚 This Week's Read",
    "philosophy": "🪶 A Thought to Carry",
    "interaction": "📣 Your Turn — Let's Connect",
    "tech": "💡 Tech Tidbit · 科技新知",
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
    "tech": "Curious by design · 每日一則科技新知",
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
