from pathlib import Path
from playwright.sync_api import sync_playwright

base = Path(__file__).resolve().parent
exports = base / "exports"
exports.mkdir(exist_ok=True)
pages = [
    "clinic-promo-flyer.html",
    "glp-lipo-onepager.html",
    "iv-membership-offer.html",
    "clinic-handout-decision-guide.html",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 1500}, device_scale_factor=2)
    for filename in pages:
        path = base / filename
        stem = path.stem
        page.goto(path.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(path=str(exports / f"{stem}.pdf"), format="Letter", print_background=True, margin={"top":"0","right":"0","bottom":"0","left":"0"})
        page.emulate_media(media="screen")
        sheet = page.locator(".sheet")
        sheet.screenshot(path=str(exports / f"{stem}.png"))
        print(f"exported {stem}")
    browser.close()
