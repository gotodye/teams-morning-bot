"""Curated famous articles and books — work performance, growth, and life mindset.

Mix of Western classics, non-business perspectives, and Asian voices (~80:20).
"""

from __future__ import annotations

from datetime import date
from typing import TypedDict


class Article(TypedDict):
    title: str
    source: str
    url: str
    topic: str
    fallback_summary: str


ARTICLES: list[Article] = [
    {
        "title": "Manage Your Energy, Not Your Time",
        "source": "Harvard Business Review",
        "url": "https://hbr.org/2007/10/manage-your-energy-not-your-time",
        "topic": "sustainable high performance at work",
        "fallback_summary": (
            "Schwartz and McCarthy show that time is fixed but personal energy can be "
            "renewed. Build rituals across physical, emotional, mental, and spiritual "
            "energy so you perform well without burning out."
        ),
    },
    {
        "title": "What Makes a Leader?",
        "source": "Harvard Business Review",
        "url": "https://hbr.org/1998/11/what-makes-a-leader",
        "topic": "emotional intelligence in leadership",
        "fallback_summary": (
            "Goleman argues that emotional intelligence — self-awareness, self-regulation, "
            "motivation, empathy, and social skill — separates great leaders from average "
            "ones more than IQ or technical skill alone."
        ),
    },
    {
        "title": "How to Build Habits That Actually Stick",
        "source": "James Clear",
        "url": "https://jamesclear.com/three-steps-habit-change",
        "topic": "building better daily habits",
        "fallback_summary": (
            "Clear explains that lasting habits need a clear cue, a craving, a simple "
            "response, and a satisfying reward. Start tiny, repeat consistently, and "
            "let identity — not willpower — drive change."
        ),
    },
    {
        "title": "The Power of Vulnerability",
        "source": "Brené Brown / TED",
        "url": "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "topic": "courage and authentic connection at work",
        "fallback_summary": (
            "Brown's research shows vulnerability is not weakness — it is the birthplace "
            "of innovation, trust, and belonging. Teams grow stronger when people can "
            "admit uncertainty and ask for help."
        ),
    },
    {
        "title": "Deep Work: Rules for Focused Success",
        "source": "Cal Newport",
        "url": "https://www.calnewport.com/books/deep-work/",
        "topic": "focused work in a distracted world",
        "fallback_summary": (
            "Newport defines deep work as distraction-free concentration that creates "
            "real value. Protect blocks of focus, reduce shallow busywork, and train "
            "attention like a skill — it compounds over a career."
        ),
    },
    {
        "title": "Man's Search for Meaning",
        "source": "Viktor E. Frankl",
        "url": "https://www.penguinrandomhouse.com/books/132832/mans-search-for-meaning-by-viktor-e-frankl/",
        "topic": "finding purpose under adversity",
        "fallback_summary": (
            "Frankl teaches that we cannot always control circumstances, but we can "
            "choose our response. A sense of meaning — in work, love, or courage — "
            "helps people endure difficulty and live with dignity."
        ),
    },
    {
        "title": "Start With Why",
        "source": "Simon Sinek",
        "url": "https://simonsinek.com/books/start-with-why/",
        "topic": "purpose-driven leadership",
        "fallback_summary": (
            "Sinek shows that inspiring leaders communicate why they exist before what "
            "they do. Purpose builds trust and loyalty — people follow causes they "
            "believe in, not just products or instructions."
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
        "title": "Grit: The Power of Passion and Perseverance",
        "source": "Angela Duckworth / TED",
        "url": "https://www.ted.com/talks/angela_lee_duckworth_grit_the_power_of_passion_and_perseverance",
        "topic": "long-term perseverance over talent",
        "fallback_summary": (
            "Duckworth defines grit as passion plus perseverance for long-term goals. "
            "Sticking with hard things — learning from setbacks and showing up again — "
            "often predicts success better than raw intelligence."
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
        "title": "The Happiness Advantage",
        "source": "Shawn Achor",
        "url": "https://www.shawnachor.com/the-books/",
        "topic": "positive psychology at work",
        "fallback_summary": (
            "Achor flips the formula: happiness fuels success, not the other way around. "
            "Small positive habits — gratitude, social connection, and optimism — "
            "improve productivity, creativity, and resilience at work."
        ),
    },
    {
        "title": "Atomic Habits: An Easy Way to Build Good Habits",
        "source": "James Clear",
        "url": "https://jamesclear.com/atomic-habits",
        "topic": "small changes that compound",
        "fallback_summary": (
            "Clear's 1% rule: tiny improvements compound into remarkable results. Design "
            "your environment, make good habits obvious and easy, and align daily actions "
            "with the person you want to become."
        ),
    },
    {
        "title": "The 7 Habits of Highly Effective People",
        "source": "Stephen R. Covey",
        "url": "https://www.franklincovey.com/the-7-habits/",
        "topic": "principles of personal effectiveness",
        "fallback_summary": (
            "Covey centers effectiveness on character and principles: be proactive, begin "
            "with the end in mind, put first things first, think win-win, and sharpen the "
            "saw through continuous renewal."
        ),
    },
    {
        "title": "Mindset: The New Psychology of Success",
        "source": "Carol S. Dweck",
        "url": "https://fs.blog/carol-dweck-mindset/",
        "topic": "growth mindset vs fixed mindset",
        "fallback_summary": (
            "Dweck shows that believing abilities can grow — a growth mindset — leads "
            "people to embrace challenges and learn from criticism. A fixed mindset "
            "avoids risk and stalls development."
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
        "title": "The Obstacle Is the Way",
        "source": "Ryan Holiday",
        "url": "https://www.thepaintedporch.com/products/the-obstacle-is-the-way",
        "topic": "stoic resilience in modern life",
        "fallback_summary": (
            "Holiday revives Stoic wisdom: obstacles are opportunities to practice "
            "perception, action, and will. Reframe setbacks, focus on what you control, "
            "and use adversity as fuel for growth."
        ),
    },
    {
        "title": "Essentialism: The Disciplined Pursuit of Less",
        "source": "Greg McKeown",
        "url": "https://gregmckeown.com/essentialism/",
        "topic": "doing less but better",
        "fallback_summary": (
            "McKeown argues for essentialism: say no to the trivial many so you can "
            "invest in the vital few. Clarity about what truly matters reduces burnout "
            "and raises the quality of your contribution."
        ),
    },
    {
        "title": "Thinking, Fast and Slow",
        "source": "Daniel Kahneman",
        "url": "https://us.macmillan.com/books/9780374533557/thinkingfastandslow",
        "topic": "decision-making and cognitive bias",
        "fallback_summary": (
            "Kahneman maps System 1 (fast, intuitive) and System 2 (slow, deliberate) "
            "thinking. Knowing when intuition misleads us — and when to pause for "
            "analysis — improves judgment at work and in life."
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
        "title": "How Will You Measure Your Life?",
        "source": "Clayton M. Christensen / Harvard Business Review",
        "url": "https://hbr.org/2010/07/how-will-you-measure-your-life",
        "topic": "aligning career choices with what matters most",
        "fallback_summary": (
            "Christensen applies management theory to life: allocate your resources — "
            "time, talent, energy — to purposes you will not regret. Integrity and "
            "relationships often matter more than short-term career optimization."
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
        "title": "The Power of Small Wins",
        "source": "Teresa Amabile / Harvard Business Review",
        "url": "https://hbr.org/2011/05/the-power-of-small-wins",
        "topic": "motivation through meaningful progress",
        "fallback_summary": (
            "Amabile's diary research shows inner work life improves when people make "
            "progress on meaningful work — even small wins. Managers who clear obstacles "
            "and celebrate forward motion unlock sustained motivation."
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
        "title": "Flow: The Psychology of Optimal Experience",
        "source": "Mihaly Csikszentmihalyi",
        "url": "https://www.penguinrandomhouse.com/books/313183/flow-by-mihaly-csikszentmihalyi/",
        "topic": "deep engagement and satisfaction in work",
        "fallback_summary": (
            "Csikszentmihalyi describes flow as complete absorption when challenge matches "
            "skill. Designing work for clear goals, immediate feedback, and focused "
            "attention increases both performance and genuine satisfaction."
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
]


def pick_article(today: date) -> Article:
    """Pick one article — half-year batch, sequential on article days."""
    from content_batch import pick_article_entry

    return pick_article_entry(today)  # type: ignore[return-value]
