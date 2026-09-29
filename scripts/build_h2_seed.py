#!/usr/bin/env python3
"""One-off builder: writes scripts/seeds/h2_2026.py from inline curated data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANAGEMENT = [
    '💼 Management Moment: "The single biggest problem in communication is the illusion that it has taken place." — George Bernard Shaw',
    '💼 Management Moment: "Alone we can do so little; together we can do so much." — Helen Keller',
    '💼 Management Moment: "The measure of intelligence is the ability to change." — Albert Einstein',
    '💼 Management Moment: "I don\'t believe in taking right decisions. I take decisions and then make them right." — Ratan Tata',
    '💼 Management Moment: "The best executive is the one who has sense enough to pick good people to do what he wants done." — Theodore Roosevelt',
    '💼 Management Moment: "Don\'t find fault, find a remedy." — Henry Ford',
    '💼 Management Moment: "Outstanding leaders go out of their way to boost the self-esteem of their personnel." — Sam Walton',
    '💼 Management Moment: "The most dangerous leadership myth is that leaders are born." — Warren Bennis',
    '💼 Management Moment: "Love your job, but never fall in love with your company — because you never know when the company stops loving you." — N. R. Narayana Murthy',
    '💼 Management Moment: "To handle yourself, use your head; to handle others, use your heart." — Eleanor Roosevelt',
    '💼 Management Moment: "Integrity is the most valuable and respected quality of leadership." — Brian Tracy',
    '💼 Management Moment: "Before you are a leader, success is all about growing yourself. When you become a leader, success is all about growing others." — Jack Welch',
    '💼 Management Moment: "The key to successful leadership today is influence, not authority." — Kenneth Blanchard',
    '💼 Management Moment: "The mission of a business is to contribute to the progress and welfare of society." — Konosuke Matsushita',
    '💼 Management Moment: "Leadership is the capacity to translate vision into reality." — Warren Bennis',
    '💼 Management Moment: "In every decision, ask yourself what is the right thing to do as a human being." — Kazuo Inamori',
    '💼 Management Moment: "If your actions inspire others to dream more, learn more, do more and become more, you are a leader." — John Quincy Adams',
    '💼 Management Moment: "The first responsibility of a leader is to define reality. The last is to say thank you." — Max De Pree',
    '💼 Management Moment: "In the midst of chaos, there is also opportunity." — Sun Tzu',
    '💼 Management Moment: "The speed of the boss is the speed of the team." — Lee Iacocca',
    '💼 Management Moment: "You manage things; you lead people." — Grace Hopper',
    '💼 Management Moment: "The best leaders are those most interested in surrounding themselves with people smarter than they are." — John C. Maxwell',
    '💼 Management Moment: "Leadership is solving problems. The day people stop bringing you their problems is the day you have stopped leading them." — Colin Powell',
    '💼 Management Moment: "Leadership is hard to define, and good leadership even harder. But if you can get people to follow you to the ends of the earth, you are a great leader." — Indra Nooyi',
    '💼 Management Moment: "A leader\'s job is not to do the work for others, it\'s to help others figure out how to do it themselves." — Simon Sinek',
    '💼 Management Moment: "The growth and development of people is the highest calling of leadership." — Harvey S. Firestone',
    '💼 Management Moment: "The pessimist complains about the wind. The optimist expects it to change. The leader adjusts the sails." — John Maxwell',
]

PHILOSOPHY = [
    '🪶 Philosophy Moment: "Be the change that you wish to see in the world." — Mahatma Gandhi',
    '🪶 Philosophy Moment: "In the middle of difficulty lies opportunity." — Albert Einstein',
    '🪶 Philosophy Moment: "The only thing we have to fear is fear itself." — Franklin D. Roosevelt',
    '🪶 Philosophy Moment: "Life can only be understood backwards; but it must be lived forwards." — Søren Kierkegaard',
    '🪶 Philosophy Moment: "Grind iron with enough patience, and one day it becomes a needle." — Vietnamese proverb',
    '🪶 Philosophy Moment: "Happiness depends upon ourselves." — Aristotle',
    '🪶 Philosophy Moment: "Liberty lies in the rights of that person whose views you find most odious." — John Stuart Mill',
    '🪶 Philosophy Moment: "Little by little, over time it becomes a hill." — Indonesian proverb',
    '🪶 Philosophy Moment: "He who fights with monsters should look to it that he himself does not become a monster." — Friedrich Nietzsche',
    '🪶 Philosophy Moment: "Go slowly, and you will get a beautiful blade." — Thai proverb',
    '🪶 Philosophy Moment: "I can control my passions and emotions if I can understand their nature." — Baruch Spinoza',
    '🪶 Philosophy Moment: "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion." — Albert Camus',
    '🪶 Philosophy Moment: "It is not death that a man should fear, but never beginning to live." — Marcus Aurelius',
    '🪶 Philosophy Moment: "Happiness is not something ready made. It comes from your own actions." — Dalai Lama',
]

ARTICLES = [
    {
        "title": "The Checklist Manifesto",
        "source": "Atul Gawande",
        "url": "https://atulgawande.com/book/the-checklist-manifesto/",
        "topic": "reducing errors through simple systems",
        "fallback_summary": (
            "Gawande shows how well-designed checklists prevent avoidable mistakes in "
            "complex work — from surgery to aviation. Discipline and humility beat "
            "relying on memory alone when stakes are high."
        ),
    },
    {
        "title": "Ikigai: The Japanese Secret to a Long and Happy Life",
        "source": "Héctor García & Francesc Miralles",
        "url": "https://ikigaibook.com/",
        "topic": "finding purpose in everyday life",
        "fallback_summary": (
            "Drawing on Japan's longest-living communities, the authors frame ikigai as "
            "the reason you get up in the morning — the overlap of what you love, what "
            "you're good at, and what the day needs. Small daily purpose beats grand plans."
        ),
    },
    {
        "title": "The Five Dysfunctions of a Team",
        "source": "Patrick Lencioni",
        "url": "https://www.tablegroup.com/books/dysfunctions",
        "topic": "building trust and accountability on teams",
        "fallback_summary": (
            "Lencioni maps how absence of trust, fear of conflict, and lack of commitment "
            "undermine teams. Vulnerability-based trust is the foundation for honest "
            "debate and shared results."
        ),
    },
    {
        "title": "The Courage to Be Disliked",
        "source": "Ichiro Kishimi & Fumitake Koga",
        "url": "https://www.simonandschuster.com/books/The-Courage-to-Be-Disliked/Ichiro-Kishimi/9781501197277",
        "topic": "freedom, self-acceptance, and Adlerian psychology",
        "fallback_summary": (
            "Framed as a dialogue, this bestseller from Japan argues that happiness is a "
            "present-tense choice, not a prize for pleasing everyone. Separating your tasks "
            "from others' opinions is where real freedom begins."
        ),
    },
    {
        "title": "The Progress Principle",
        "source": "Teresa Amabile & Steven Kramer",
        "url": "https://hbr.org/2011/05/the-power-of-small-wins",
        "topic": "motivation through meaningful daily progress",
        "fallback_summary": (
            "Amabile and Kramer found that the strongest workplace motivator is making "
            "meaningful progress on work that matters — even small wins compound into "
            "engagement and creativity."
        ),
    },
    {
        "title": "Thanks for the Feedback",
        "source": "Douglas Stone & Sheila Heen",
        "url": "https://www.stoneandheen.com/thanks-for-the-feedback",
        "topic": "receiving and using feedback well",
        "fallback_summary": (
            "Stone and Heen teach that growth depends on how we receive feedback, not "
            "just how we give it. Separating triggers from useful signal helps people "
            "learn without defensiveness."
        ),
    },
    {
        "title": "The Coaching Habit",
        "source": "Michael Bungay Stanier",
        "url": "https://boxofcrayons.com/the-coaching-habit/",
        "topic": "leading through questions instead of advice",
        "fallback_summary": (
            "Stanier offers seven essential questions that help managers coach in ten "
            "minutes or less. Staying curious longer reduces over-helping and builds "
            "other people's problem-solving muscle."
        ),
    },
    {
        "title": "Crucial Conversations",
        "source": "Kerry Patterson et al.",
        "url": "https://cruciallearning.com/crucial-conversations/",
        "topic": "dialogue when stakes and emotions run high",
        "fallback_summary": (
            "The authors show how to stay in dialogue when opinions differ and emotions "
            "are strong. Safety, shared purpose, and clear stories prevent conflict from "
            "derailing important decisions."
        ),
    },
    {
        "title": "The Culture Code",
        "source": "Daniel Coyle",
        "url": "https://danielcoyle.com/the-culture-code/",
        "topic": "building psychological safety and belonging",
        "fallback_summary": (
            "Coyle studies high-performing groups and finds three skills: building safety, "
            "sharing vulnerability, and establishing purpose. Belonging cues matter more "
            "than talent alone."
        ),
    },
    {
        "title": "The Life-Changing Magic of Tidying Up",
        "source": "Marie Kondo",
        "url": "https://konmari.com/marie-kondo-books/",
        "topic": "clarity through keeping only what sparks joy",
        "fallback_summary": (
            "Kondo's KonMari method is really about decision-making: keep what adds value, "
            "thank and release the rest. A tidy space — or inbox, or task list — frees "
            "attention for what actually matters."
        ),
    },
    {
        "title": "The Infinite Game",
        "source": "Simon Sinek",
        "url": "https://simonsinek.com/books/the-infinite-game/",
        "topic": "long-term purpose over short-term wins",
        "fallback_summary": (
            "Sinek contrasts finite games played to win with infinite games played to "
            "keep going. Just cause, trusting teams, and worthy rivals sustain organizations "
            "beyond quarterly metrics."
        ),
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "source": "Yuval Noah Harari",
        "url": "https://www.ynharari.com/book/sapiens-2/",
        "topic": "how shared stories let humans cooperate at scale",
        "fallback_summary": (
            "Harari argues our superpower is fiction: money, nations, and companies are "
            "shared stories that let strangers cooperate. Understanding the narratives we "
            "live inside helps us question — and redesign — them."
        ),
    },
    {
        "title": "The Hard Thing About Hard Things",
        "source": "Ben Horowitz",
        "url": "https://www.harpercollins.com/products/the-hard-thing-about-hard-things-ben-horowitz",
        "topic": "leading through uncertainty and crisis",
        "fallback_summary": (
            "Horowitz shares unfiltered lessons on firing friends, managing fear, and "
            "making decisions with incomplete information. Leadership is often lonely "
            "work done without a playbook."
        ),
    },
    {
        "title": "Nonviolent Communication",
        "source": "Marshall B. Rosenberg",
        "url": "https://www.cnvc.org/learn/resources/books",
        "topic": "empathy and clear requests at work",
        "fallback_summary": (
            "Rosenberg teaches observations without judgment, naming feelings and needs, "
            "and making clear requests. This reduces defensiveness and helps teams resolve "
            "conflict without winners and losers."
        ),
    },
    {
        "title": "Why We Sleep",
        "source": "Matthew Walker",
        "url": "https://www.simonandschuster.com/books/Why-We-Sleep/Matthew-Walker/9781501144325",
        "topic": "how rest powers focus, mood, and health",
        "fallback_summary": (
            "Walker gathers decades of science showing sleep is not lost time but the "
            "foundation of learning, memory, and emotional balance. Protecting rest is one "
            "of the highest-return habits for real productivity."
        ),
    },
    {
        "title": "The Power of Moments",
        "source": "Chip Heath & Dan Heath",
        "url": "https://heathbrothers.com/books/the-power-of-moments/",
        "topic": "designing memorable experiences at work",
        "fallback_summary": (
            "The Heath brothers show how defining moments share peaks, pride, and "
            "connection. Small thoughtful gestures — onboarding, recognition, transitions "
            "— disproportionately shape how people feel."
        ),
    },
    {
        "title": "The Tao of Pooh",
        "source": "Benjamin Hoff",
        "url": "https://www.penguinrandomhouse.com/books/56949/the-tao-of-pooh-by-benjamin-hoff/",
        "topic": "Taoist simplicity through Winnie-the-Pooh",
        "fallback_summary": (
            "Hoff explains Taoism using Pooh as the model of effortless ease: work with "
            "things as they are, not against them. Doing less — but at the right moment — "
            "is often wiser than forcing outcomes."
        ),
    },
    {
        "title": "Switch: How to Change Things When Change Is Hard",
        "source": "Chip Heath & Dan Heath",
        "url": "https://heathbrothers.com/books/switch/",
        "topic": "behavior change for individuals and teams",
        "fallback_summary": (
            "Switch frames change as directing the rider, motivating the elephant, and "
            "shaping the path. Clear direction plus emotional buy-in and environment "
            "design make new habits stick."
        ),
    },
    {
        "title": "Quiet: The Power of Introverts",
        "source": "Susan Cain",
        "url": "https://www.quietrev.com/the-book",
        "topic": "valuing introverted strengths at work",
        "fallback_summary": (
            "Cain challenges the extrovert ideal and highlights deep thinking, listening, "
            "and preparation as leadership strengths. Teams perform better when both "
            "quiet and vocal styles have room."
        ),
    },
    {
        "title": "The Art of Happiness",
        "source": "Dalai Lama & Howard C. Cutler",
        "url": "https://www.penguinrandomhouse.com/books/163977/the-art-of-happiness-by-dalai-lama-and-howard-c-cutler/",
        "topic": "training the mind toward contentment",
        "fallback_summary": (
            "A psychiatrist interviews the Dalai Lama on living well. The core idea: "
            "happiness is a skill built through compassion, perspective, and daily mental "
            "habits — less a stroke of luck than a practice."
        ),
    },
    {
        "title": "Team of Teams",
        "source": "General Stanley McChrystal",
        "url": "https://www.penguinrandomhouse.com/books/316183/team-of-teams-by-general-stanley-mcchrystal-with-tantum-collins-david-silverman-and-chris-fussell/",
        "topic": "adaptive leadership in fast-changing environments",
        "fallback_summary": (
            "McChrystal argues that rigid hierarchies fail against fast-moving problems. "
            "Shared consciousness and empowered execution let teams act like networks "
            "instead of silos."
        ),
    },
    {
        "title": "The First 90 Days",
        "source": "Michael D. Watkins",
        "url": "https://hbr.org/books/watkins",
        "topic": "successful transitions into new roles",
        "fallback_summary": (
            "Watkins offers a roadmap for accelerating learning, securing early wins, and "
            "negotiating success in a new position. Transition failures are costly — "
            "preparation beats improvisation."
        ),
    },
    {
        "title": "Show Your Work!",
        "source": "Austin Kleon",
        "url": "https://austinkleon.com/show-your-work/",
        "topic": "sharing your process to grow and connect",
        "fallback_summary": (
            "Kleon argues you don't need to be a genius — you need to be findable. Sharing "
            "small pieces of your work-in-progress builds skill, feedback, and a network "
            "far better than waiting for the perfect finished thing."
        ),
    },
    {
        "title": "Multipliers: How the Best Leaders Make Everyone Smarter",
        "source": "Liz Wiseman",
        "url": "https://www.wisemaninstitute.com/multipliers",
        "topic": "amplifying team intelligence as a leader",
        "fallback_summary": (
            "Wiseman contrasts leaders who drain capability with those who multiply it. "
            "Multipliers ask hard questions, delegate ownership, and create room for "
            "others to contribute their best thinking."
        ),
    },
    {
        "title": "Range: Why Generalists Triumph in a Specialized World",
        "source": "David Epstein",
        "url": "https://davidepstein.com/the-range/",
        "topic": "why broad experience beats early specialization",
        "fallback_summary": (
            "Epstein shows that in complex, unpredictable fields, people who sample widely "
            "and connect across domains often outperform early specialists. Detours and "
            "varied interests are features of growth, not detours from it."
        ),
    },
    {
        "title": "The Lean Startup",
        "source": "Eric Ries",
        "url": "https://theleanstartup.com/",
        "topic": "validated learning and iterative improvement",
        "fallback_summary": (
            "Ries advocates build-measure-learn loops instead of big-bang launches. Small "
            "experiments reduce waste and help teams discover what customers actually value."
        ),
    },
    {
        "title": "Man's Search for Meaning",
        "source": "Viktor E. Frankl",
        "url": "https://www.penguinrandomhouse.com/books/132832/mans-search-for-meaning-by-viktor-e-frankl/",
        "topic": "finding purpose even in hardship",
        "fallback_summary": (
            "Frankl, a psychiatrist and Holocaust survivor, argues that we can't always "
            "choose our circumstances, but we can always choose our response. A sense of "
            "meaning — in work, love, or courage — is what carries people through the hard days."
        ),
    },
]

INTERACTIONS = [
    {
        "headline": "Weekend Recharge",
        "kind": "channel",
        "body": "What recharged you this past weekend — sleep, people, nature, or something else? One line is plenty.",
        "channel_fallback": "",
    },
    {
        "headline": "Skill Spotlight",
        "kind": "channel",
        "body": "What's one skill you're quietly getting better at this month? Share the skill and one tiny habit helping you practice it.",
        "channel_fallback": "",
    },
    {
        "headline": "Helpful Habit",
        "kind": "channel",
        "body": "Drop one work habit that made your last two weeks smoother — even if it's as small as a calendar block or a keyboard shortcut.",
        "channel_fallback": "",
    },
    {
        "headline": "Hometown Breakfast",
        "kind": "channel",
        "body": "What does a typical breakfast look like where you grew up? A dish, a drink, a photo — let's take a little tour of the team's tables. 🍳🍜",
        "channel_fallback": "",
    },
    {
        "headline": "Collaboration Win",
        "kind": "channel",
        "body": "Name one moment in the last two weeks when teamwork made the outcome better than going solo. What made it work?",
        "channel_fallback": "",
    },
    {
        "headline": "Focus Trick",
        "kind": "channel",
        "body": "What's your best trick for a focused hour — headphones, timer, walking, inbox closed? Steal ideas from each other in the replies.",
        "channel_fallback": "",
    },
    {
        "headline": "Kindness Ledger",
        "kind": "channel",
        "body": "Share one small act of kindness you noticed recently — given, received, or observed. Let's collect good receipts.",
        "channel_fallback": "",
    },
    {
        "headline": "Untranslatable Word",
        "kind": "channel",
        "body": "Teach us one word or phrase from your language that's hard to translate — and what it really means. 🌏",
        "channel_fallback": "",
    },
    {
        "headline": "Reset Ritual",
        "kind": "channel",
        "body": "After a tough day, what helps you reset — walk, music, tea, boundary? Share a ritual that actually works for you.",
        "channel_fallback": "",
    },
    {
        "headline": "Proud Moment",
        "kind": "channel",
        "body": "What's one thing you're quietly proud of from the last two weeks? Progress counts even if nobody applauded yet.",
        "channel_fallback": "",
    },
    {
        "headline": "Advice to Past Self",
        "kind": "channel",
        "body": "If you could send one sentence of advice to yourself on your first day in this role, what would it say?",
        "channel_fallback": "",
    },
    {
        "headline": "Team Superpower",
        "kind": "channel",
        "body": "What do you think this team's unofficial superpower is — speed, care, humor, precision? Reply with one word and one example.",
        "channel_fallback": "",
    },
    {
        "headline": "Gratitude Round",
        "kind": "channel",
        "body": "Name one person and one non-person thing you're grateful for this week. Keep it work-appropriate and heartfelt.",
        "channel_fallback": "",
    },
    {
        "headline": "Perspective Shift",
        "kind": "channel",
        "body": "When did you last change your mind about something at work? What new evidence or conversation helped you see it differently?",
        "channel_fallback": "",
    },
]


def _static() -> list[dict]:
    items: list[dict] = [
        # --- Humor (de-engineered, workplace + life) ---
        {"text": "Your calendar is full, but your coffee cup is fuller. Priorities. ☕", "format": "humor", "mood": "humor"},
        {"text": "The snooze button is a negotiator with terrible terms. You still showed up. 👏", "format": "humor", "mood": "humor"},
        {"text": "Today's forecast: 80% chance of meetings that could have been an email. ☁️", "format": "humor", "mood": "humor"},
        {"text": "Your inbox is not a to-do list — it's a suggestion box from the universe. 📥", "format": "humor", "mood": "humor"},
        {"text": "Reminder: you are not a printer. Low toner is not a personality. 🖨️", "format": "humor", "mood": "humor"},
        {"text": "The office plant is thriving on pure neglect. Some of us relate deeply. 🪴", "format": "humor", "mood": "humor"},
        {"text": "Autocorrect changed my mood to 'moist' and honestly, for a Monday, that tracks. 😅", "format": "humor", "mood": "humor"},
        # --- Warm + a micro-challenge ---
        {"text": "You don't need a perfect morning — just an honest start and one kind choice. 🌤️", "format": "warm", "mood": "warm"},
        {"text": "Someone on your team is glad you're here today, even if they haven't said it yet. 💬", "format": "warm", "mood": "warm"},
        {"text": "Progress is still progress when nobody claps. Keep going quietly if you need to. 👣", "format": "warm", "mood": "warm"},
        {"text": "A deep breath costs nothing and quietly upgrades most conversations. 🌬️", "format": "warm", "mood": "warm"},
        {"text": "You have handled hard weeks before. This one gets your experience, not your fear. 💪", "format": "warm", "mood": "warm"},
        {"text": "Micro-challenge: in your first meeting today, ask one real question before offering an answer. Notice what shifts. 🎯", "format": "warm", "mood": "action"},
        # --- Facts (some with a reply hook, some Asia-flavored) ---
        {"text": "Octopuses have three hearts — which one is keeping yours going this morning? Reply with what's fueling you. 🐙", "format": "fact", "mood": "cute"},
        {"text": "Sea otters hold hands while sleeping so they don't drift apart. Teamwork, illustrated. 🦦", "format": "fact", "mood": "cute"},
        {"text": "Indonesia is spread across 17,000+ islands. You don't have to do everything today — just island-hop one task at a time. 🏝️", "format": "fact", "mood": "nature"},
        {"text": "Vietnam is the world's 2nd-largest coffee exporter. Somewhere, your morning cup is quietly saying cảm ơn. ☕", "format": "fact", "mood": "culture"},
        {"text": "Thailand's calendar runs 543 years ahead — over there it's already the 2560s. You're basically working from the future. 🗓️", "format": "fact", "mood": "culture"},
        {"text": "Your brain uses about 20% of your body's energy. Fuel it kindly this morning. 🧠", "format": "fact", "mood": "science"},
        {"text": "A group of flamingos is called a flamboyance. May your stand-up be equally confident. 🦩", "format": "fact", "mood": "cute"},
    ]
    travel = [
        (
            "Son Doong Cave, Vietnam 🇻🇳\nThe world's largest cave hides its own jungle, river, and clouds underground.\nSome of the biggest things stay quiet until you go looking.",
            "Son Doong Cave Vietnam largest cave jungle",
        ),
        (
            "Raja Ampat, Indonesia 🇮🇩\nJade islands scatter across glass-clear sea at the edge of the map.\nThe best places rarely sit on the shortest route.",
            "Raja Ampat Indonesia islands aerial turquoise",
        ),
        (
            "Kawah Ijen, Indonesia 🇮🇩\nElectric-blue flames flicker from the crater before dawn — fire the color of the sea.\nRare sights reward the early riser.",
            "Kawah Ijen blue fire volcano Indonesia",
        ),
        (
            "Mù Cang Chải, Vietnam 🇻🇳\nTerraced hillsides ripple gold at harvest, each curve shaped by generations of hands.\nSteady effort, season after season, carves something beautiful.",
            "Mu Cang Chai Vietnam rice terraces golden",
        ),
        (
            "Batad Rice Terraces, Philippines 🇵🇭\nStone-walled steps climb the mountains like a 2,000-year-old staircase to the clouds.\nPatience, stacked high enough, becomes a wonder.",
            "Batad rice terraces Philippines amphitheater",
        ),
        (
            "Bagan, Myanmar 🇲🇲\nThousands of pagodas rise from morning mist like prayers left standing in gold light.\nQuiet wonder travels well across time zones.",
            "Bagan Myanmar temples sunrise balloons",
        ),
        (
            "Socotra Island, Yemen 🇾🇪\nDragon-blood trees spread like umbrellas on a landscape that looks borrowed from another planet.\nStrange and rare can still be exactly right.",
            "Socotra Island Yemen dragon blood trees",
        ),
        (
            "Tsingy de Bemaraha, Madagascar 🇲🇬\nLimestone blades rise into a forest of stone you can only cross by rope and nerve.\nSome paths are earned, not strolled.",
            "Tsingy de Bemaraha Madagascar stone forest",
        ),
        (
            "Chefchaouen, Morocco 🇲🇦\nAn entire town washed in a hundred shades of blue, tucked into the Rif Mountains.\nA little color can change the whole mood of a place.",
            "Chefchaouen Morocco blue city streets",
        ),
        (
            "Salar de Uyuni, Bolivia 🇧🇴\nAfter rain, the salt flats mirror the sky until earth and heaven trade places.\nPerspective is a place you can visit.",
            "Salar de Uyuni Bolivia salt flats mirror",
        ),
        (
            "Zhangye Danxia, China 🇨🇳\nHills striped in red, gold, and turquoise, painted slowly over millions of years.\nBeauty layered patiently outlasts anything rushed.",
            "Zhangye Danxia rainbow mountains China",
        ),
        (
            "Caño Cristales, Colombia 🇨🇴\nFor a few weeks a year, a river blushes red, yellow, and green — the 'liquid rainbow'.\nRare timing is its own kind of magic.",
            "Cano Cristales Colombia river of five colors",
        ),
        (
            "Lençóis Maranhenses, Brazil 🇧🇷\nWhite dunes cradle turquoise lagoons that appear only after the rains.\nEven a desert keeps a little water for the right moment.",
            "Lencois Maranhenses Brazil dunes lagoons",
        ),
        (
            "Wadi Rum, Jordan 🇯🇴\nRose sand and vast silence stretch wider than any to-do list can travel.\nStep into the morning unhurried.",
            "Wadi Rum Jordan desert red sand",
        ),
        (
            "Tiger's Nest, Bhutan 🇧🇹\nA monastery clings to a cliff above the clouds, reached only on foot.\nSome heights are meant to be climbed slowly, and on purpose.",
            "Paro Taktsang Tiger's Nest Bhutan monastery",
        ),
    ]
    for text, query in travel:
        items.append({"text": text, "format": "travel", "image_query": query})

    extras = [
        # --- Humor ---
        {"text": "Thursday energy: not quite Friday, but the trailer looks promising. 🎬", "format": "humor", "mood": "humor"},
        {"text": "The office thermostat has three settings: Arctic, Sahara, and 'who touched this'. 🌡️", "format": "humor", "mood": "humor"},
        {"text": "Meetings are like clouds — some bring rain, some just block the sun. Aim to be neither. ☁️", "format": "humor", "mood": "humor"},
        {"text": "Coffee: because adulting requires a loading screen. ☕", "format": "humor", "mood": "humor"},
        {"text": "Your future self already thanked you for starting the hard task first. Weird timeline, great choice. ⏳", "format": "humor", "mood": "humor"},
        {"text": "Weekend loading… please keep a little kindness cached for Monday. 💾", "format": "humor", "mood": "humor"},
        # --- Warm + a micro-challenge ---
        {"text": "If your week were a playlist, today is the bridge track — still moving. 🎵", "format": "warm", "mood": "warm"},
        {"text": "You made it this far with your humor intact. That genuinely counts. 🎉", "format": "warm", "mood": "warm"},
        {"text": "Done lists beat perfect plans every single time. ✅", "format": "warm", "mood": "warm"},
        {"text": "Kindness is free, remembered, and weirdly contagious. Start a small outbreak today. 💛", "format": "warm", "mood": "warm"},
        {"text": "Rest isn't the reward for finishing — it's part of how good work gets made. 🌙", "format": "warm", "mood": "warm"},
        {"text": "Micro-challenge: send one colleague a specific thank-you before lunch. Specific beats generic. 🙏", "format": "warm", "mood": "action"},
        # --- Facts (Asia-flavored + reply hooks) ---
        {"text": "Crows can recognize human faces for years. Be memorable for the right reasons. 🐦‍⬛", "format": "fact", "mood": "nature"},
        {"text": "Trees share nutrients through underground fungal networks. Collaboration is older than email. 🌳", "format": "fact", "mood": "nature"},
        {"text": "Taipei 101 rides out typhoons on a giant golden pendulum. Balance under pressure is a design choice. 🏙️", "format": "fact", "mood": "architecture"},
        {"text": "The world's largest flower, the Rafflesia, blooms in the forests of Sumatra — rare things are worth the wait. 🌺", "format": "fact", "mood": "nature"},
        {"text": "Honey never spoils — jars 3,000 years old were found still edible. Patience keeps well. 🍯", "format": "fact", "mood": "science"},
        {"text": "Bananas are berries, but strawberries aren't. Botany is chaos — what's your plot twist today? 🍌", "format": "fact", "mood": "nature"},
        # --- Travel (more rare gems) ---
        {
            "text": "Pamukkale, Turkey 🇹🇷\nWhite mineral terraces spill down the hillside like frozen waterfalls of milk.\nBeauty can be built one gentle layer at a time.",
            "format": "travel",
            "image_query": "Pamukkale Turkey white travertine terraces",
        },
        {
            "text": "Kelimutu, Indonesia 🇮🇩\nThree crater lakes on one volcano, each a different color — and the colors quietly change.\nNot everything needs to stay the same to be at peace.",
            "format": "travel",
            "image_query": "Kelimutu crater lakes Flores Indonesia",
        },
    ]
    items.extend(extras)
    return items


def main() -> int:
    batch = {
        "management": MANAGEMENT,
        "philosophy": PHILOSOPHY,
        "articles": ARTICLES,
        "interactions": INTERACTIONS,
        "static": _static(),
    }
    out = ROOT / "scripts" / "seeds" / "h2_2026.py"
    payload = json.dumps(batch, ensure_ascii=False, indent=4)
    out.write_text(
        '"""Curated seed content for 2026-H2 (Jul–Dec). All new vs 2026-H1."""\n\n'
        "from __future__ import annotations\n\n"
        "from typing import Any\n\n\n"
        f"BATCH: dict[str, Any] = {payload}\n\n\n"
        "def get_batch() -> dict[str, Any]:\n"
        "    return BATCH\n",
        encoding="utf-8",
    )
    print(f"Wrote {out} with counts:", {k: len(v) for k, v in batch.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
