import os
import re
import shutil
import zipfile
from pathlib import Path


def safe_name(name):
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", name)
    name = re.sub(r"-+", "-", name)
    return name.strip("-_") or "blackout-project"


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def choose_menu(title_text, options):
    print(f"\n╔══ {title_text} ══╗")
    for key, value in options.items():
        print(f"  {key}. {value}")
    print("╚" + "═" * (len(title_text) + 8) + "╝")

    while True:
        choice = input("Pilih: ").strip()
        if choice in options:
            return choice
        print("Pilihan tidak valid.")


def get_project_type():
    return choose_menu(
        "PROJECT TYPE",
        {
            "1": "Professional Portfolio",
            "2": "Business Landing Page",
            "3": "School Website",
        },
    )


def get_style():
    return choose_menu(
        "DESIGN STYLE",
        {
            "1": "Modern",
            "2": "Glass",
            "3": "Dark Premium",
            "4": "Gradient",
        },
    )


def default_color(style):
    return {
        "1": "#38bdf8",
        "2": "#8b5cf6",
        "3": "#60a5fa",
        "4": "#06b6d4",
    }.get(style, "#38bdf8")


def generate_css(primary, style):
    if style == "2":
        background = "#07111f"
        surface = "rgba(255,255,255,.07)"
        border = "rgba(255,255,255,.12)"
    elif style == "3":
        background = "#05070b"
        surface = "#0d1117"
        border = "#202938"
    else:
        background = "#f5f7fb"
        surface = "#ffffff"
        border = "#e5e7eb"

    gradient = f"linear-gradient(135deg, {primary}, #6366f1)"

    return f"""\
:root {{
    --primary: {primary};
    --gradient: {gradient};
    --bg: {background};
    --surface: {surface};
    --border: {border};
    --text: #f8fafc;
    --muted: #94a3b8;
    --radius: 20px;
    --shadow: 0 20px 60px rgba(0,0,0,.12);
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
    font-family: Inter, ui-sans-serif, system-ui, -apple-system,
        BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
}}

a {{
    color: inherit;
    text-decoration: none;
}}

.container {{
    width: min(1120px, calc(100% - 40px));
    margin-inline: auto;
}}

.navbar {{
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(18px);
    background: rgba(5, 7, 11, .72);
    border-bottom: 1px solid var(--border);
}}

.nav-inner {{
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.logo {{
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: -.03em;
}}

.logo span {{
    color: var(--primary);
}}

.nav-links {{
    display: flex;
    align-items: center;
    gap: 26px;
    color: #cbd5e1;
    font-size: .95rem;
}}

.nav-links a {{
    transition: .2s ease;
}}

.nav-links a:hover {{
    color: var(--primary);
}}

.menu-btn {{
    display: none;
    border: 0;
    background: transparent;
    color: white;
    font-size: 1.5rem;
}}

.hero {{
    min-height: 720px;
    display: grid;
    place-items: center;
    position: relative;
    overflow: hidden;
}}

.hero::before {{
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    background: var(--primary);
    opacity: .12;
    filter: blur(120px);
    border-radius: 50%;
}}

.hero-content {{
    position: relative;
    max-width: 820px;
    text-align: center;
}}

.badge {{
    display: inline-flex;
    padding: 8px 14px;
    border: 1px solid var(--border);
    border-radius: 999px;
    color: var(--primary);
    background: var(--surface);
    font-size: .85rem;
    margin-bottom: 24px;
}}

.hero h1 {{
    font-size: clamp(3rem, 8vw, 6.5rem);
    line-height: .95;
    letter-spacing: -.065em;
    margin-bottom: 26px;
}}

.hero h1 span {{
    background: var(--gradient);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.hero p {{
    max-width: 650px;
    margin: auto;
    color: var(--muted);
    font-size: 1.1rem;
}}

.actions {{
    display: flex;
    justify-content: center;
    gap: 14px;
    margin-top: 34px;
    flex-wrap: wrap;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
    padding: 0 22px;
    border-radius: 12px;
    font-weight: 700;
    transition: transform .2s ease, box-shadow .2s ease;
}}

.btn:hover {{
    transform: translateY(-3px);
}}

.btn-primary {{
    color: white;
    background: var(--gradient);
    box-shadow: 0 12px 35px rgba(56,189,248,.18);
}}

.btn-secondary {{
    border: 1px solid var(--border);
    background: var(--surface);
}}

.section {{
    padding: 110px 0;
}}

.section-head {{
    max-width: 650px;
    margin-bottom: 45px;
}}

.section-head span {{
    color: var(--primary);
    font-weight: 700;
}}

.section-head h2 {{
    margin-top: 10px;
    font-size: clamp(2rem, 5vw, 3.5rem);
    letter-spacing: -.05em;
}}

.section-head p {{
    margin-top: 14px;
    color: var(--muted);
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}

.card {{
    padding: 28px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
    box-shadow: var(--shadow);
    transition: transform .25s ease, border-color .25s ease;
}}

.card:hover {{
    transform: translateY(-7px);
    border-color: var(--primary);
}}

.card-icon {{
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: rgba(56,189,248,.12);
    color: var(--primary);
    margin-bottom: 22px;
    font-size: 1.25rem;
}}

.card h3 {{
    margin-bottom: 10px;
}}

.card p {{
    color: var(--muted);
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}

.stat {{
    padding: 28px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface);
}}

.stat strong {{
    display: block;
    font-size: 2.4rem;
}}

.stat span {{
    color: var(--muted);
}}

.cta {{
    padding: 55px;
    border-radius: 30px;
    background: var(--gradient);
    color: white;
    text-align: center;
}}

.cta h2 {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    letter-spacing: -.05em;
}}

.cta p {{
    margin: 12px auto 25px;
    max-width: 600px;
    opacity: .85;
}}

.cta .btn {{
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
    transform: translateY(24px);
    transition: .7s ease;
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.glass-mode {{
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.16), transparent 30%),
        #05070b;
}}

@media (max-width: 800px) {{
    .nav-links {{
        position: absolute;
        top: 72px;
        left: 20px;
        right: 20px;
        display: none;
        flex-direction: column;
        padding: 20px;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: #0b111a;
    }}

    .nav-links.open {{
        display: flex;
    }}

    .menu-btn {{
        display: block;
    }}

    .grid,
    .stats {{
        grid-template-columns: 1fr;
    }}

    .hero {{
        min-height: 650px;
    }}

    .section {{
        padding: 80px 0;
    }}

    .cta {{
        padding: 35px 24px;
    }}
}}
"""


def generate_js():
    return """\
const menuButton = document.querySelector(".menu-btn");
const navLinks = document.querySelector(".nav-links");

if (menuButton && navLinks) {
    menuButton.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });

    navLinks.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("open");
        });
    });
}

const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    },
    { threshold: 0.12 }
);

document.querySelectorAll(".reveal").forEach((element) => {
    observer.observe(element);
});

console.log("BLACKOUT Professional Website");
"""


def generate_html(name, project_type, style):
    if project_type == "1":
        badge = "PERSONAL PORTFOLIO"
        title = f"Hi, I'm <span>{name}</span>."
        description = (
            "A modern professional portfolio built with clean design, "
            "responsive layouts and smooth interactions."
        )
        cards = """
        <article class="card reveal">
            <div class="card-icon">01</div>
            <h3>Web Development</h3>
            <p>Building responsive and modern web experiences.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">02</div>
            <h3>UI Design</h3>
            <p>Creating interfaces focused on clarity and usability.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">03</div>
            <h3>Problem Solving</h3>
            <p>Turning ideas into practical digital products.</p>
        </article>
        """
        section_title = "What I Do"

    elif project_type == "2":
        badge = "DIGITAL BUSINESS"
        title = f"Build something <span>remarkable.</span>"
        description = (
            "A professional business landing page designed to present "
            "your brand, services and value proposition."
        )
        cards = """
        <article class="card reveal">
            <div class="card-icon">01</div>
            <h3>Strategy</h3>
            <p>Clear digital strategies designed around your goals.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">02</div>
            <h3>Solutions</h3>
            <p>Simple, effective and scalable digital solutions.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">03</div>
            <h3>Growth</h3>
            <p>Helping ideas grow through better digital experiences.</p>
        </article>
        """
        section_title = "Our Services"

    else:
        badge = "MODERN SCHOOL"
        title = f"Welcome to <span>{name}</span>."
        description = (
            "A modern school website concept for information, "
            "programs, activities and digital communication."
        )
        cards = """
        <article class="card reveal">
            <div class="card-icon">01</div>
            <h3>Programs</h3>
            <p>Explore educational programs and learning opportunities.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">02</div>
            <h3>Activities</h3>
            <p>Discover student activities, events and communities.</p>
        </article>
        <article class="card reveal">
            <div class="card-icon">03</div>
            <h3>Information</h3>
            <p>Access important school information in one place.</p>
        </article>
        """
        section_title = "Explore"

    extra_class = "glass-mode" if style == "2" else ""

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="{name} - Professional website generated by BLACKOUT.">
    <title>{name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="{extra_class}">

<header class="navbar">
    <div class="container nav-inner">
        <a href="#" class="logo">{name}<span>.</span></a>
        <button class="menu-btn" aria-label="Open menu">☰</button>
        <nav class="nav-links">
            <a href="#home">Home</a>
            <a href="#services">Services</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </nav>
    </div>
</header>

<main>
<section class="hero" id="home">
    <div class="container hero-content reveal">
        <div class="badge">{badge}</div>
        <h1>{title}</h1>
        <p>{description}</p>
        <div class="actions">
            <a href="#services" class="btn btn-primary">Explore</a>
            <a href="#contact" class="btn btn-secondary">Get Started</a>
        </div>
    </div>
</section>

<section class="section" id="services">
    <div class="container">
        <div class="section-head reveal">
            <span>FEATURES</span>
            <h2>{section_title}</h2>
            <p>
                Everything is designed to look clean,
                professional and easy to use.
            </p>
        </div>
        <div class="grid">
            {cards}
        </div>
    </div>
</section>

<section class="section" id="about">
    <div class="container">
        <div class="section-head reveal">
            <span>ABOUT</span>
            <h2>Built for the modern web.</h2>
            <p>
                Lightweight architecture, responsive design
                and polished interactions.
            </p>
        </div>
        <div class="stats">
            <div class="stat reveal">
                <strong>100%</strong>
                <span>Responsive</span>
            </div>
            <div class="stat reveal">
                <strong>Fast</strong>
                <span>Lightweight</span>
            </div>
            <div class="stat reveal">
                <strong>Clean</strong>
                <span>Code structure</span>
            </div>
        </div>
    </div>
</section>

<section class="section" id="contact">
    <div class="container">
        <div class="cta reveal">
            <h2>Ready to build?</h2>
            <p>
                This website was generated locally by BLACKOUT.
                Customize the content and make it yours.
            </p>
            <a href="mailto:hello@example.com" class="btn">
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

<script src="js/app.js"></script>
</body>
</html>
"""


def generate_readme(name, project_type):
    return f"""\
# {name}

Professional website generated by BLACKOUT Project Generator.

## Project Type

{project_type}

## Structure

```text
{safe_name(name)}/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── app.js
├── assets/
└── README.md
```

## Run

Open `index.html` in a browser.

## Generated By

BLACKOUT
"""


def create_project():
    print("""
╔══════════════════════════════════════════╗
║     BLACKOUT PROFESSIONAL GENERATOR     ║
║                 V1.0                    ║
╚══════════════════════════════════════════╝
""")

    project_name = ask("Nama project", "My Website")
    project_type = get_project_type()
    style = get_style()

    primary = ask("Primary color HEX", default_color(style))

    folder_name = safe_name(project_name)

    output_root = Path.home() / "blackout-projects"
    project_dir = output_root / folder_name
    zip_path = output_root / f"{folder_name}.zip"

    if project_dir.exists():
        overwrite = ask("Project sudah ada. Timpa? (y/n)", "n").lower()
        if overwrite != "y":
            print("Dibatalkan.")
            return
        shutil.rmtree(project_dir)

    if zip_path.exists():
        zip_path.unlink()

    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "css").mkdir()
    (project_dir / "js").mkdir()
    (project_dir / "assets").mkdir()

    type_name = {
        "1": "Professional Portfolio",
        "2": "Business Landing Page",
        "3": "School Website",
    }[project_type]

    (project_dir / "index.html").write_text(
        generate_html(project_name, project_type, style),
        encoding="utf-8",
    )

    (project_dir / "css" / "style.css").write_text(
        generate_css(primary, style),
        encoding="utf-8",
    )

    (project_dir / "js" / "app.js").write_text(
        generate_js(),
        encoding="utf-8",
    )

    (project_dir / "README.md").write_text(
        generate_readme(project_name, type_name),
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
                    file.relative_to(output_root),
                )

    print("""
╔══════════════════════════════════════════╗
║          PROJECT BERHASIL DIBUAT        ║
╚══════════════════════════════════════════╝
""")
    print(f"Folder : {project_dir}")
    print(f"ZIP    : {zip_path}")
    print(f"\nBuka : cd '{project_dir}'")
    print("\nProject siap digunakan.")


def project_generator():
    try:
        create_project()
    except KeyboardInterrupt:
        print("\nGenerator dibatalkan.")
    except Exception as exc:
        print(f"\nERROR: {exc}")


if __name__ == "__main__":
    project_generator()
