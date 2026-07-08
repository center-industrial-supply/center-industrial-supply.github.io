#!/usr/bin/env python3
"""DEPRECATED: Use Astro build instead (npm run build).

This script is kept for reference. Main pages are now Astro components in src/pages/.
Legacy archive pages in public/ use layout.js for header/footer injection.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#022b33">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/site.css">
  <link rel="icon" href="{prefix}wp-content/uploads/2020/10/small-brand-logo-1024x194.png">
</head>
<body class="cisc-body">
"""

FOOT = """
  <script src="{prefix}assets/js/site.js"></script>
</body>
</html>
"""

CATEGORIES = [
    ("Standard Equipment", "MIG, TIG, MMA, plasma, and multi-process welders", "product-category/standard-equipment/index.html", "64", "⚙"),
    ("Welding Consumables", "Electrodes, wires, flux, and filler metals", "product-category/welding-consumables/index.html", "", "🔥"),
    ("Engine Driven Welders", "Portable engine-driven welding power sources", "product-category/engine-driven-welder/index.html", "4", "🔧"),
    ("Welding Automation", "Carriages, submerged arc, columns, gantries", "product-category/standard-welding-automation/index.html", "14", "🤖"),
    ("Robot Systems", "Welding robots, positioners, material handling", "product-category/robot-systems/index.html", "10", "🦾"),
    ("CNC Cutting & Drilling", "Plasma, laser, plate and beam CNC machines", "product-category/cutting-drilling-automation/index.html", "11", "✂️"),
    ("Tube & Pipe Solutions", "Orbital cutting, bevelling, and welding systems", "product-category/tube-and-pipe-cutting-and-welding-solutions/index.html", "37", "🔗"),
    ("Induction Heating", "Pre-heat and post-heat induction systems", "product-category/induction-heating-machine/index.html", "6", "🌡"),
    ("PPE & Accessories", "Helmets, gloves, spectacles, and safety gear", "product-category/ppe-and-accessories/index.html", "19", "🦺"),
    ("Laser Welding", "Advanced laser welding technology", "product-category/laser-welding/index.html", "1", "✨"),
    ("Welding & Cutting Torches", "Manual torches and cutting equipment", "product-category/welding-and-cutting-torch/index.html", "2", "🔦"),
    ("Stud Welding", "Stud welding machines and accessories", "product-category/stud-welding-equipment/index.html", "3", "📌"),
]

BRANDS = [
    "ESAB", "GYS", "OTC", "Hypertherm", "AMG", "Aotai", "Kjellberg",
    "MOSA", "Shindaiwa", "Weldflame", "Wilson", "Hgstar", "IKING", "Exact",
]


def load_partial(name: str, prefix: str) -> str:
    text = (ROOT / "assets" / "partials" / f"{name}.html").read_text(encoding="utf-8")
    return text.replace("{{PREFIX}}", prefix)


def page_shell(title: str, description: str, prefix: str, body: str) -> str:
    return HEAD.format(title=title, description=description, prefix=prefix) + load_partial("header", prefix) + body + load_partial("footer", prefix) + FOOT.format(prefix=prefix)


def category_cards(prefix: str) -> str:
    items = []
    for name, desc, href, count, icon in CATEGORIES:
        count_html = f'<span class="cisc-category-card__count">{count} products</span>' if count else ""
        items.append(
            f"""<a class="cisc-category-card" href="{prefix}{href}">
  <div class="cisc-category-card__icon" aria-hidden="true">{icon}</div>
  <h3>{name}</h3>
  <p>{desc}</p>
  {count_html}
</a>"""
        )
    return "\n".join(items)


def brand_pills() -> str:
    return "\n".join(f'<span class="cisc-brand">{b}</span>' for b in BRANDS)


def write_homepage() -> None:
    prefix = ""
    body = f"""
<main>
  <section class="cisc-hero">
    <div class="cisc-hero__bg" aria-hidden="true"></div>
    <div class="cisc-hero__grid" aria-hidden="true"></div>
    <div class="cisc-container cisc-hero__content">
      <span class="cisc-hero__eyebrow">Since 1957</span>
      <h1>Welding &amp; Cutting Solutions for Philippine Industry</h1>
      <p class="cisc-hero__lead">Center Industrial Supply Corporation distributes world-class welding equipment, consumables, and automation systems — backed by technical expertise and service you can count on.</p>
      <div class="cisc-hero__actions">
        <a class="cisc-btn cisc-btn--primary" href="{prefix}products/index.html">Browse Products</a>
        <a class="cisc-btn cisc-btn--outline" href="{prefix}contact-us/index.html">Request a Quote</a>
      </div>
    </div>
  </section>

  <section class="cisc-stats">
    <div class="cisc-container cisc-stats__grid">
      <div><div class="cisc-stat__number">65+</div><div class="cisc-stat__label">Years of Service</div></div>
      <div><div class="cisc-stat__number">150+</div><div class="cisc-stat__label">Products in Catalog</div></div>
      <div><div class="cisc-stat__number">20+</div><div class="cisc-stat__label">Global Brands</div></div>
      <div><div class="cisc-stat__number">1</div><div class="cisc-stat__label">Technology Center</div></div>
    </div>
  </section>

  <section class="cisc-section">
    <div class="cisc-container">
      <div class="cisc-section__header">
        <div class="cisc-section__eyebrow">Product Categories</div>
        <h2>Equipment for Every Welding &amp; Cutting Process</h2>
        <p>From manual welding to fully automated robotic systems — find the right solution for your application.</p>
      </div>
      <div class="cisc-categories">{category_cards(prefix)}</div>
    </div>
  </section>

  <section class="cisc-section cisc-section--alt">
    <div class="cisc-container">
      <div class="cisc-split">
        <div>
          <div class="cisc-section__eyebrow">About CISC</div>
          <h2>More Than a Supplier — A Solutions Partner</h2>
          <p>We represent global brands who are leaders in process development and advanced technology. Our commitment to integrity, innovative technology, and outstanding technical support has made us a trusted name in Philippine industry for over six decades.</p>
          <p>Our product range covers practically all welding and cutting processes — from high-performance manual equipment to advanced digital machines and fully-automated robotics.</p>
          <a class="cisc-btn cisc-btn--dark" href="{prefix}about-us/index.html">Our Story</a>
        </div>
        <div class="cisc-split__image">
          <img src="{prefix}wp-content/uploads/2020/10/secondary-guy-industrial.jpg" alt="Welding professional at work" width="600" height="360">
        </div>
      </div>
    </div>
  </section>

  <section class="cisc-section">
    <div class="cisc-container">
      <div class="cisc-section__header">
        <div class="cisc-section__eyebrow">Authorized Brands</div>
        <h2>World-Class Manufacturers</h2>
        <p>We partner with industry-leading brands to bring you proven technology and reliable performance.</p>
      </div>
      <div class="cisc-brands">{brand_pills()}</div>
    </div>
  </section>

  <section class="cisc-section cisc-section--alt">
    <div class="cisc-container">
      <div class="cisc-section__header">
        <div class="cisc-section__eyebrow">Why Choose Us</div>
        <h2>Built on Service &amp; Expertise</h2>
      </div>
      <div class="cisc-features">
        <div class="cisc-feature">
          <div class="cisc-feature__icon" aria-hidden="true">🎯</div>
          <h3>Process Expertise</h3>
          <p>Decades of application knowledge across shipbuilding, fabrication, automotive, oil &amp; gas, and more.</p>
        </div>
        <div class="cisc-feature">
          <div class="cisc-feature__icon" aria-hidden="true">🏭</div>
          <h3>Technology Center</h3>
          <p>Demo, training, and process development facility in Filinvest Technology Park, Calamba, Laguna.</p>
        </div>
        <div class="cisc-feature">
          <div class="cisc-feature__icon" aria-hidden="true">🛠</div>
          <h3>After-Sales Support</h3>
          <p>Timely, reliable service and technical support — because we view every customer as a long-term partner.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cisc-cta">
    <div class="cisc-container">
      <h2>Need Help Choosing Equipment?</h2>
      <p>Our technical team can recommend the right welding or cutting solution for your application.</p>
      <a class="cisc-btn cisc-btn--outline" href="{prefix}contact-us/index.html">Get in Touch</a>
    </div>
  </section>
</main>
"""
    (ROOT / "index.html").write_text(page_shell(
        "Center Industrial Supply Corporation — Welding & Cutting Equipment",
        "Philippines' leading distributor of welding and cutting equipment, consumables, automation, and robotic systems since 1957.",
        prefix,
        body,
    ), encoding="utf-8")


def write_about() -> None:
    prefix = "../"
    body = f"""
<header class="cisc-page-header">
  <div class="cisc-container">
    <div class="cisc-breadcrumb"><a href="{prefix}index.html">Home</a> / About Us</div>
    <h1>About Us</h1>
  </div>
</header>
<main class="cisc-section">
  <div class="cisc-container">
    <div class="cisc-split" style="margin-bottom:3rem">
      <div class="cisc-prose">
        <h2>Introduction</h2>
        <p>Center Industrial Supply Corporation is a leading welding and cutting products distributor in the Philippines. Representing global brands who are leaders in process development and advanced technology, we pride ourselves with being not only a supplier but primarily a solutions provider to Philippine industries for over six decades now.</p>
        <p>Behind our success and reputation is our commitment to integrity, innovative technology, process expertise, customer focus, and outstanding service and technical support.</p>
        <p>Our product range includes welding and cutting equipment, consumables and accessories for practically all welding and cutting processes. Equipment in our line range from simple yet high-performance manual equipment, to the more advanced digital-based machines, to fully-automated systems and robotics.</p>
        <p>Our products provide solutions in a wide range of applications and industries: sheet metal fabrication, heavy steel fabrication, automotive, shipbuilding, offshore oil and gas, boiler, construction, cement, mining, sugar and many more.</p>
      </div>
      <div class="cisc-split__image">
        <img src="{prefix}wp-content/uploads/2020/10/cisc-logo-full.png" alt="Center Industrial Supply Corporation" width="500" height="120" style="object-fit:contain;background:#eaedf0;padding:2rem">
      </div>
    </div>

    <h2>Our History</h2>
    <div class="cisc-timeline">
      <div class="cisc-timeline__item">
        <div class="cisc-timeline__year">1957</div>
        <p>Founder Mr. Doy Ting opens Center Construction Supply along Azcarraga Street (now Claro M. Recto Avenue) in Sta. Cruz, Manila — beginning our journey in welding and industrial supply.</p>
      </div>
      <div class="cisc-timeline__item">
        <div class="cisc-timeline__year">Growth</div>
        <p>The company expands its product portfolio and representation of international welding brands, establishing a reputation for technical expertise across Philippine industries.</p>
      </div>
      <div class="cisc-timeline__item">
        <div class="cisc-timeline__year">Today</div>
        <p>Headquartered in Quezon City with a Technology Center in Calamba, Laguna, CISC continues to deliver welding, cutting, and automation solutions backed by demonstration, training, and after-sales service.</p>
      </div>
    </div>
  </div>
</main>
"""
    (ROOT / "about-us" / "index.html").write_text(page_shell(
        "About Us — Center Industrial Supply Corporation",
        "Learn about Center Industrial Supply Corporation — a leading welding and cutting distributor serving Philippine industries since 1957.",
        prefix,
        body,
    ), encoding="utf-8")


def write_products() -> None:
    prefix = "../"
    body = f"""
<header class="cisc-page-header">
  <div class="cisc-container">
    <div class="cisc-breadcrumb"><a href="{prefix}index.html">Home</a> / Products</div>
    <h1>Products</h1>
    <p style="opacity:.9;margin:0">Welding equipment, consumables, automation, and safety products for every application.</p>
  </div>
</header>
<main class="cisc-section">
  <div class="cisc-container">
    <div class="cisc-categories">{category_cards(prefix)}</div>
    <p style="text-align:center;margin-top:2.5rem"><a class="cisc-btn cisc-btn--primary" href="{prefix}all-products/index.html">View Full Product Catalog</a></p>
  </div>
</main>
"""
    (ROOT / "products" / "index.html").write_text(page_shell(
        "Products — Center Industrial Supply Corporation",
        "Browse welding equipment, cutting machines, consumables, robotics, PPE, and automation solutions from Center Industrial Supply.",
        prefix,
        body,
    ), encoding="utf-8")


def write_support() -> None:
    prefix = "../"
    body = f"""
<header class="cisc-page-header">
  <div class="cisc-container">
    <div class="cisc-breadcrumb"><a href="{prefix}index.html">Home</a> / Support</div>
    <h1>Support &amp; Service</h1>
  </div>
</header>
<main class="cisc-section">
  <div class="cisc-container">
    <div class="cisc-support-grid">
      <div class="cisc-support-card">
        <h3>Technology Center</h3>
        <p>Our Technology Center in Filinvest Technology Park, Calamba, Laguna combines demo, process development, and training under one roof. Experience our innovative welding and cutting solutions first-hand.</p>
      </div>
      <div class="cisc-support-card">
        <h3>Service &amp; Repair</h3>
        <p>We view our customers as partners and put high value on timely, reliable, after-sales service support. Our service team is always available to help keep your equipment running.</p>
      </div>
      <div class="cisc-support-card">
        <h3>Demonstrations</h3>
        <p>We showcase the latest manual and automated welding and cutting technology — helping customers achieve increased productivity and improved quality.</p>
      </div>
    </div>
    <div class="cisc-cta" style="margin-top:3rem;border-radius:6px">
      <h2>Schedule a Demo or Service Visit</h2>
      <p>Contact our team to arrange equipment demonstrations, technical consultations, or service support.</p>
      <a class="cisc-btn cisc-btn--outline" href="{prefix}contact-us/index.html">Contact Support</a>
    </div>
  </div>
</main>
"""
    (ROOT / "support" / "index.html").write_text(page_shell(
        "Support — Center Industrial Supply Corporation",
        "Technology Center, demonstrations, training, and after-sales service for welding and cutting equipment in the Philippines.",
        prefix,
        body,
    ), encoding="utf-8")


def write_contact() -> None:
    prefix = "../"
    body = f"""
<header class="cisc-page-header">
  <div class="cisc-container">
    <div class="cisc-breadcrumb"><a href="{prefix}index.html">Home</a> / Contact</div>
    <h1>Contact Us</h1>
  </div>
</header>
<main class="cisc-section">
  <div class="cisc-container">
    <div class="cisc-contact-grid">
      <div class="cisc-contact-card">
        <h3>Head Office</h3>
        <ul class="cisc-contact-list">
          <li><div><strong>Address</strong>10 South AA Street, Quezon City, Metro Manila, Philippines 1103</div></li>
          <li><div><strong>Phone</strong><a href="tel:+63283739651">(02) 8373-9651</a>, <a href="tel:+63234168688">3416-8688</a>, <a href="tel:+63234156097">3415-6097</a></div></li>
          <li><div><strong>Fax</strong>(02) 8373-4211</div></li>
          <li><div><strong>Email</strong><a href="mailto:info@centerindustrial.com">info@centerindustrial.com</a></div></li>
        </ul>
      </div>
      <div class="cisc-contact-card">
        <h3>Working Hours</h3>
        <table class="cisc-hours">
          <tr><th>Monday</th><td>7:30 AM – 5:30 PM</td></tr>
          <tr><th>Tuesday</th><td>7:30 AM – 5:30 PM</td></tr>
          <tr><th>Wednesday</th><td>7:30 AM – 5:30 PM</td></tr>
          <tr><th>Thursday</th><td>7:30 AM – 5:30 PM</td></tr>
          <tr><th>Friday</th><td>7:30 AM – 5:30 PM</td></tr>
          <tr><th>Saturday</th><td>Closed</td></tr>
          <tr><th>Sunday</th><td>Closed</td></tr>
        </table>
        <p style="margin-top:1.5rem">Connect with us on <a href="https://www.facebook.com/CenterIndustrialSupply/" target="_blank" rel="noopener">Facebook</a></p>
      </div>
    </div>
    <div class="cisc-contact-card" style="margin-top:2rem">
      <h3>Product Inquiries</h3>
      <p>For product quotes and technical questions, please reach us by phone or email. Our representatives will respond as soon as possible. <em>(Online contact forms from the original site are not available in this static archive rebuild.)</em></p>
    </div>
  </div>
</main>
"""
    (ROOT / "contact-us" / "index.html").write_text(page_shell(
        "Contact Us — Center Industrial Supply Corporation",
        "Contact Center Industrial Supply in Quezon City for welding equipment quotes, technical support, and product inquiries.",
        prefix,
        body,
    ), encoding="utf-8")


def write_all_products() -> None:
    prefix = "../"
    # Extract product links from existing archive
    products = []
    for path in sorted((ROOT / "product").rglob("index.html")):
        html = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.parent.relative_to(ROOT).as_posix()
        title_m = re.search(r"<title>([^<]+)</title>", html)
        h3_m = re.search(r'class=product-title[^>]*>([^<]+)', html)
        name = h3_m.group(1).strip() if h3_m else (title_m.group(1).split(" - ")[0] if title_m else path.parent.name)
        img_m = re.search(r'wp-content/uploads/[^"\']+\.(?:jpg|png|webp)', html)
        img = img_m.group(0) if img_m else "wp-content/uploads/woocommerce-placeholder.png"
        brand_m = re.search(r'product-brand-container[^>]*>\s*<span>([^<]+)', html)
        brand = brand_m.group(1).strip() if brand_m else ""
        products.append((name, rel, img, brand))

    cards = []
    for name, rel, img, brand in products:
        brand_html = f'<div class="cisc-product-card__brand">{brand}</div>' if brand else ""
        cards.append(
            f"""<a class="cisc-product-card" href="{prefix}{rel}/index.html">
  <div class="cisc-product-card__img"><img src="{prefix}{img}" alt="{name}" loading="lazy" width="300" height="300"></div>
  <div class="cisc-product-card__body">{brand_html}<h3>{name}</h3></div>
</a>"""
        )

    body = f"""
<header class="cisc-page-header">
  <div class="cisc-container">
    <div class="cisc-breadcrumb"><a href="{prefix}index.html">Home</a> / All Products</div>
    <h1>All Products</h1>
    <p style="opacity:.9;margin:0">{len(products)} products recovered from archive</p>
  </div>
</header>
<main class="cisc-section">
  <div class="cisc-container">
    <div class="cisc-product-grid">
{chr(10).join(cards)}
    </div>
  </div>
</main>
"""
    (ROOT / "all-products" / "index.html").write_text(page_shell(
        "All Products — Center Industrial Supply Corporation",
        "Full product catalog of welding and cutting equipment from Center Industrial Supply Corporation.",
        prefix,
        body,
    ), encoding="utf-8")
    print(f"Catalog: {len(products)} products")


LEGACY_INJECT = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/site.css">
<link rel="stylesheet" href="{prefix}assets/css/legacy.css">
<script defer src="{prefix}assets/js/layout.js"></script>
"""


def depth_prefix(path: Path) -> str:
    rel = path.parent.relative_to(ROOT)
    if str(rel) == ".":
        return ""
    depth = len(rel.parts)
    return "../" * depth


def strip_legacy_inject(html: str) -> str:
    return re.sub(
        r"<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">.*?<script defer src=\"[^\"]*assets/js/layout\.js\"></script>",
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )


def inject_legacy_assets(html: str, prefix: str) -> str:
    inject = LEGACY_INJECT.format(prefix=prefix)
    html = strip_legacy_inject(html)
    doctype = re.search(r"<!doctype[^>]*>", html, re.IGNORECASE)
    if doctype:
        pos = doctype.end()
        return html[:pos] + inject + html[pos:]
    if re.search(r"<head\b", html, re.IGNORECASE):
        return re.sub(r"(<head[^>]*>)", r"\1" + inject, html, count=1, flags=re.IGNORECASE)
    return inject + html


def enhance_legacy_pages() -> int:
    skip_dirs = {"assets", "scripts", "fonts.googleapis.com", "fonts.gstatic.com", ".git"}
    skip_files = {
        ROOT / "index.html",
        ROOT / "about-us" / "index.html",
        ROOT / "products" / "index.html",
        ROOT / "support" / "index.html",
        ROOT / "contact-us" / "index.html",
        ROOT / "all-products" / "index.html",
    }
    count = 0
    for path in ROOT.rglob("index.html"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path in skip_files:
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        prefix = depth_prefix(path)
        updated = inject_legacy_assets(html, prefix)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count


def main() -> None:
    write_homepage()
    write_about()
    write_products()
    write_support()
    write_contact()
    write_all_products()
    enhanced = enhance_legacy_pages()
    print(f"Enhanced {enhanced} legacy pages")


if __name__ == "__main__":
    main()
