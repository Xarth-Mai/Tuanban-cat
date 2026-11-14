"""Optional browser regression checks for file:// and HTTP. Not a site runtime dependency.

python -m pip install playwright
python -m playwright install chromium
python tests/browser_check.py [--screenshots /path/outside/repository]
Uses an installed system Chromium when available. Never contacts external URLs.
"""
from pathlib import Path
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import shutil
import threading

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def check(screenshots=None, http_only=False):
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which("chromium"), args=["--no-sandbox"])
            urls = [f"http://127.0.0.1:{server.server_port}/"]
            if not http_only:
                urls.insert(0, (ROOT / "index.html").as_uri())
            for url in urls:
                page = browser.new_page(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
                errors, external = [], []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("request", lambda request: external.append(request.url)
                        if request.url.startswith(("http://", "https://")) and not request.url.startswith("http://127.0.0.1:") else None)
                page.goto(url)
                expect(page.locator(".sticker-card")).to_have_count(12)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.locator('[data-category="happy"]').click()
                expect(page.locator(".sticker-card")).to_have_count(3)
                page.locator("#search").fill("爱心")
                expect(page.locator(".sticker-card")).to_have_count(1)
                page.locator(".sticker-preview").click()
                expect(page.locator("#sticker-dialog")).to_be_visible()
                expect(page.locator("#dialog-title")).to_have_text("开心小心心")
                expect(page.locator("#dialog-image")).to_have_attribute("src", "assets/stickers/happy/happy-heart.webp")
                with page.expect_download() as info:
                    page.locator("#dialog-download").click()
                download = info.value
                assert download.suggested_filename == "happy-heart.webp"
                assert download.failure() is None
                page.keyboard.press("Escape")
                expect(page.locator("#sticker-dialog")).not_to_be_visible()
                page.locator("#search").fill("")
                page.locator(".sticker-preview").first.click()
                first = page.locator("#dialog-title").text_content()
                page.keyboard.press("ArrowRight")
                assert page.locator("#dialog-title").text_content() != first
                page.keyboard.press("Escape")
                expect(page.locator("#filters button")).to_have_count(5)
                expect(page.locator('[data-category="sleepy"]')).to_have_count(0)
                expect(page.locator("#collection-summary")).to_contain_text("12 张")
                page.locator("#search").fill("")
                page.locator('[data-category="all"]').click()
                expect(page.locator(".sticker-card")).to_have_count(12)
                page.locator("#search").fill("找不到的猫猫词")
                expect(page.locator("#empty-state")).to_be_visible()
                page.locator("#reset-filters").click()
                page.evaluate("Promise.all([...document.images].map(img => {img.loading='eager'; return img.decode();}))")
                assert page.locator("img").evaluate_all("images => images.every(i => i.complete && i.naturalWidth > 0)")
                assert not errors, errors
                assert not external, external
                if screenshots and (http_only or url.startswith("file:")):
                    screenshots.mkdir(parents=True, exist_ok=True)
                    page.evaluate("window.scrollTo(0,0)")
                    page.screenshot(path=str(screenshots / "desktop.png"))
                page.set_viewport_size({"width": 390, "height": 844})
                page.evaluate("window.scrollTo(0,0)")
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile overflow"
                page.locator(".sticker-preview").first.click()
                expect(page.locator("#sticker-dialog")).to_be_visible()
                page.locator("#dialog-close").click()
                if screenshots and (http_only or url.startswith("file:")):
                    page.evaluate("window.scrollTo(0,0)")
                    page.screenshot(path=str(screenshots / "mobile.png"))
                page.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    protocols = "HTTP only (file:// blocked by environment policy)" if http_only else "file:// and HTTP"
    print(f"PASS: {protocols}; 12 images, category/search, empty states, modal/keyboard, downloads, mobile, no external requests.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screenshots", type=Path)
    parser.add_argument("--http-only", action="store_true", help="Use when the environment prohibits file URLs")
    args = parser.parse_args()
    check(args.screenshots, args.http_only)
