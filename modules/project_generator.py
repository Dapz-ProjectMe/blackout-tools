import re
import shutil
import zipfile
from pathlib import Path

VERSION = "2.0"


def safe_name(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    value = re.sub(r"-+", "-", value)
    return value.strip("-_") or "blackout-project"


def ask(prompt, default=""):
    value = input(f"{prompt} [{default}]: ").strip() if default else input(f"{prompt}: ").strip()
    return value or default


def menu(title, options):
    print(f"\n=== {title} ===")
    for key, label in options.items():
        print(f"{key}. {label}")

    while True:
        choice = input("Pilih: ").strip()
        if choice in options:
            return choice
        print("Pilihan tidak valid.")


def choose_color():
    colors = {
        "1": ("Sky Blue", "#38BDF8"),
        "2": ("Blue", "#3B82F6"),
        "3": ("Purple", "#8B5CF6"),
        "4": ("Green", "#22C55E"),
        "5": ("Orange", "#F97316"),
        "6": ("Pink", "#EC4899"),
        "7": ("Red", "#EF4444"),
        "8": ("Custom HEX", None),
    }

    choice = menu("PRIMARY COLOR", {key: value[0] for key, value in colors.items()})

    if choice == "8":
        while True:
            color = input("HEX color, contoh #38BDF8: ").strip()
            if re.fullmatch(r"#[0-9a-fA-F]{6}", color):
                return color.upper()
            print("HEX tidak valid.")

    return colors[choice][1]


def get_content(project_type):
    data = {
        "1": {
            "badge": "PERSONAL PORTFOLIO",
            "section": "Featured Work",
            "cards": [
                ("01", "Web Development", "Responsive and modern websites built with clean front-end code."),
                ("02", "UI Design", "Interfaces focused on clarity, consistency and usability."),
                ("03", "Creative Projects", "Digital projects built from practical ideas."),
            ],
        },
        "2": {
            "badge": "DIGITAL BUSINESS",
            "section": "Our Services",
            "cards": [
                ("01", "Strategy", "Clear digital strategies aligned with business goals."),
                ("02", "Solutions", "Practical digital solutions for modern brands."),
                ("03", "Growth", "Better experiences that help your business grow."),
            ],
        },
        "3": {
            "badge": "MODERN SCHOOL",
            "section": "Explore",
            "cards": [
                ("01", "Programs", "Discover learning programs and opportunities."),
                ("02", "Activities", "Showcase student activities and school events."),
                ("03", "Information", "Keep students and parents connected."),
            ],
        },
        "4": {
            "badge": "DIGITAL PRODUCT",
            "section": "Why Choose Us",
            "cards": [
                ("01", "Fast", "A lightweight experience focused on speed."),
                ("02", "Powerful", "A flexible product concept ready to customize."),
                ("03", "Simple", "A clear interface that keeps important things in focus."),
            ],
        },
    }
    return data[project_type]


def make_css(primary, style):
    if style == "1":
        bg = "#f7f9fc"
        surface = "#ffffff"
        border = "#e5e7eb"
        text = "#0f172a"
        muted = "#64748b"
    elif style == "2":
        bg = "#07111f"
        surface = "rgba(255,255,255,.07)"
        border = "rgba(255,255,255,.12)"
        text = "#f8fafc"
        muted = "#94a3b8"
    elif style == "3":
        bg = "#05070b"
        surface = "#0d1117"
        border = "#202938"
        text = "#f8fafc"
        muted = "#94a3b8"
    else:
        bg = "#06111a"
        surface = "#0c1722"
        border = "rgba(255,255,255,.10)"
        text = "#f8fafc"
        muted = "#9fb0c2"

    return f"""\
:root {{
    --primary: {primary};
    --gradient: linear-gradient(135deg, {primary}, #6366f1);
    --bg: {bg};
    --surface: {surface};
    --border: {border};
    --text: {text};
    --muted: {muted};
    --radius: 22px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    min-height: 100vh;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}}

a {{
    color: inherit;
    text-decoration: none;
}}

.container {{
    width: min(1160px, calc(100% - 40px));
    margin: auto;
}}

.navbar {{
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid var(--border);
    background: var(--bg);
    backdrop-filter: blur(18px);
}}

.nav-inner {{
    min-height: 74px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.logo {{
    font-size: 1.2rem;
    font-weight: 900;
}}

.logo span {{
    color: var(--primary);
}}

.nav-links {{
    display: flex;
    gap: 28px;
    color: var(--muted);
}}

.nav-links a:hover {{
    color: var(--primary);
}}

.menu-button {{
    display: none;
    border: 0;
    background: transparent;
    color: var(--text);
    font-size: 1.5rem;
}}

.hero {{
    min-height: 720px;
    display: grid;
    place-items: center;
    text-align: center;
}}

.hero-content {{
    max-width: 900px;
}}

.badge {{
    display: inline-block;
    padding: 8px 14px;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: var(--surface);
    color: var(--primary);
    font-size: .8rem;
    font-weight: 800;
}}

.hero h1 {{
    margin-top: 25px;
    font-size: clamp(3rem, 8vw, 7rem);
    line-height: .95;
    letter-spacing: -.07em;
}}

.gradient-text {{
    background: var(--gradient);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.hero-description {{
    max-width: 680px;
    margin: 28px auto;
    color: var(--muted);
    font-size: 1.1rem;
}}

.actions {{
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
}}

.button {{
    min-height: 50px;
    padding: 0 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    border: 1px solid var(--border);
    font-weight: 800;
}}

.button-primary {{
    border-color: transparent;
    color: white;
    background: var(--gradient);
}}

.button-secondary {{
    background: var(--surface);
}}

.section {{
    padding: 100px 0;
}}

.eyebrow {{
    color: var(--primary);
    font-weight: 900;
    letter-spacing: .1em;
}}

.section-heading {{
    max-width: 700px;
    margin-bottom: 45px;
}}

.section-heading h2 {{
    margin-top: 10px;
    font-size: clamp(2.3rem, 5vw, 4rem);
    line-height: 1;
}}

.section-heading p {{
    margin-top: 16px;
    color: var(--muted);
}}

.card-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}

.card {{
    min-height: 230px;
    padding: 30px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
    transition: .25s ease;
}}

.card:hover {{
    transform: translateY(-7px);
    border-color: var(--primary);
}}

.card-number {{
    color: var(--primary);
    font-weight: 900;
}}

.card h3 {{
    margin-top: 40px;
}}

.card p {{
    margin-top: 10px;
    color: var(--muted);
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}

.stat {{
    padding: 30px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
}}

.stat strong {{
    display: block;
    font-size: 2.5rem;
}}

.stat span {{
    color: var(--muted);
}}

.cta {{
    padding: 70px 30px;
    border-radius: 30px;
    background: var(--gradient);
    color: white;
    text-align: center;
}}

.cta h2 {{
    font-size: clamp(2.3rem, 6vw, 4.5rem);
    line-height: 1;
}}

.cta p {{
    max-width: 600px;
    margin: 18px auto 28px;
}}

.cta .button {{
    background: white;
    color: #0f172a;
}}

footer {{
    padding: 35px 0;
    border-top: 1px solid var(--border);
    color: var(--muted);
    text-align: center;
}}

.reveal {{
    opacity: 0;
    transform: translateY(22px);
    transition: .7s ease;
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

@media (max-width: 820px) {{
    .menu-button {{
        display: block;
    }}

    .nav-links {{
        position: absolute;
        top: 74px;
        left: 20px;
        right: 20px;
        display: none;
        flex-direction: column;
        padding: 18px;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: var(--bg);
    }}

    .nav-links.open {{
        display: flex;
    }}

    .card-grid,
    .stats {{
        grid-template-columns: 1fr;
    }}
}}
"""


def make_js():
    return """\
const button = document.querySelector(".menu-button");
const nav = document.querySelector(".nav-links");

button?.addEventListener("click", () => {
    nav?.classList.toggle("open");
});

nav?.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
        nav.classList.remove("open");
    });
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((element) => {
    observer.observe(element);
});
"""


def make_html(name, tagline, description, data):
    cards = ""

    for number, title, text in data["cards"]:
        cards += f"""
            <article class="card reveal">
                <div class="card-number">{number}</div>
                <h3>{title}</h3>
                <p>{text}</p>
            </article>
"""

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<header class="navbar">
    <div class="container nav-inner">
        <a class="logo" href="#home">{name}<span>.</span></a>

        <button class="menu-button" type="button">
            ☰
        </button>

        <nav class="nav-links">
            <a href="#home">Home</a>
            <a href="#work">Work</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </nav>
    </div>
</header>

<main>

<section class="hero" id="home">
    <div class="container hero-content reveal">
        <div class="badge">{data["badge"]}</div>

        <h1>
            {tagline}
            <br>
            <span class="gradient-text">{name}</span>
        </h1>

        <p class="hero-description">{description}</p>

        <div class="actions">
            <a class="button button-primary" href="#work">Explore</a>
            <a class="button button-secondary" href="#contact">
                Get Started
            </a>
        </div>
    </div>
</section>

<section class="section" id="work">
    <div class="container">
        <div class="section-heading reveal">
            <div class="eyebrow">FEATURES</div>
            <h2>{data["section"]}</h2>
            <p>
                A professional foundation that you can customize
                with your own content and branding.
            </p>
        </div>

        <div class="card-grid">
{cards}
        </div>
    </div>
</section>

<section class="section" id="about">
    <div class="container">
        <div class="section-heading reveal">
            <div class="eyebrow">ABOUT</div>
            <h2>Simple. Fast. Professional.</h2>
            <p>
                Built with plain HTML, CSS and JavaScript.
                No API is required.
            </p>
        </div>

        <div class="stats">
            <div class="stat reveal">
                <strong>100%</strong>
                <span>Responsive</span>
            </div>

            <div class="stat reveal">
                <strong>0</strong>
                <span>Required APIs</span>
            </div>

            <div class="stat reveal">
                <strong>3</strong>
                <span>Core technologies</span>
            </div>
        </div>
    </div>
</section>

<section class="section" id="contact">
    <div class="container">
        <div class="cta reveal">
            <h2>Ready to make it yours?</h2>
            <p>
                Customize the generated files and publish your
                website anywhere you want.
            </p>

            <a class="button" href="mailto:hello@example.com">
                Contact
            </a>
        </div>
    </div>
</section>

</main>

<footer>
    <div class="container">
        © 2026 {name}. Generated by BLACKOUT.
    </div>
</footer>

<script src="js/script.js"></script>
</body>
</html>
"""


def create_project():
    print(f"""
╔══════════════════════════════════════════╗
║     BLACKOUT PROJECT GENERATOR V{VERSION}      ║
╚══════════════════════════════════════════╝
""")

    name = ask("Nama project", "My Website")
    tagline = ask("Tagline utama", "Build something remarkable.")
    description = ask(
        "Deskripsi singkat",
        "A modern professional website built with BLACKOUT."
    )

    project_type = menu(
        "PROJECT TYPE",
        {
            "1": "Professional Portfolio",
            "2": "Business Landing Page",
            "3": "School Website",
            "4": "Product Landing Page",
        },
    )

    style = menu(
        "DESIGN STYLE",
        {
            "1": "Modern",
            "2": "Glass",
            "3": "Dark Premium",
            "4": "Gradient",
        },
    )

    color = choose_color()
    data = get_content(project_type)

    root = Path.home() / "blackout-projects"
    root.mkdir(parents=True, exist_ok=True)

    folder_name = safe_name(name)
    project_dir = root / folder_name
    zip_path = root / f"{folder_name}.zip"

    if project_dir.exists():
        answer = ask("Project sudah ada. Timpa? (y/n)", "n").lower()
        if answer != "y":
            print("Dibatalkan.")
            return

        shutil.rmtree(project_dir)

    if zip_path.exists():
        zip_path.unlink()

    (project_dir / "css").mkdir(parents=True)
    (project_dir / "js").mkdir()
    (project_dir / "assets").mkdir()

    (project_dir / "index.html").write_text(
        make_html(name, tagline, description, data),
        encoding="utf-8",
    )

    (project_dir / "css" / "style.css").write_text(
        make_css(color, style),
        encoding="utf-8",
    )

    (project_dir / "js" / "script.js").write_text(
        make_js(),
        encoding="utf-8",
    )

    (project_dir / "README.md").write_text(
        f"""# {name}

Generated by BLACKOUT Project Generator V{VERSION}.

No OpenAI API is required.

## Run locally

```bash
python -m http.server 8080
```

Then open the local address shown by Python.
""",
        encoding="utf-8",
    )

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as archive:
        for file in project_dir.rglob("*"):
            if file.is_file():
                archive.write(
                    file,
                    file.relative_to(root),
                )

    print("""
╔══════════════════════════════════════════╗
║       ✓ WEBSITE BERHASIL DIBUAT         ║
╚══════════════════════════════════════════╝
""")
    print(f"Folder : {project_dir}")
    print(f"ZIP    : {zip_path}")
    print("\nPreview:")
    print(f'cd "{project_dir}"')
    print("python -m http.server 8080")
    print("\nOpenAI API tidak diperlukan.")


def project_generator():
    try:
        create_project()
    except KeyboardInterrupt:
        print("\nGenerator dibatalkan.")
    except Exception as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    project_generator()
