# HR Connect website (v1)

This folder holds the static marketing website for HR Connect: 42 pages, plus a 404 page, `sitemap.xml` and `robots.txt`.

## Editing pages

Don't edit the generated `index.html` files by hand. Change the source and rebuild:

- `_build/content.py` holds all page text, navigation, footer and site settings.
- `_build/build.py` holds the layout and the building blocks pages are made from.
- `assets/css/site.css` holds the styles.
- `assets/js/site.js` handles the menu, forms and search boxes.
- `assets/js/calculators.js` holds the three free calculators.

To rebuild after a change:

```bash
python3 website-v1/_build/build.py
```

## Previewing

Pages use clean URLs (`/product/payroll/`), so open them through a local server rather than by double-clicking:

```bash
python3 -m http.server 8000 --directory website-v1
```

Then open http://localhost:8000.

## Before going live

1. Set `SITE_URL`, `APP_URL` and `CONTACT_EMAIL` at the top of `_build/content.py`. They are placeholders: `www.hrconnect.ai`, `app.hrconnect.ai` and `hello@hrconnect.ai`.
2. Connect the forms (Book a demo, Contact, Partners) to a form service or the backend. Until then they open the visitor's email app.
3. Add prices on the Pricing page. It currently says "Custom quote".
4. Have the legal drafts reviewed: Privacy, Terms and Cookies.
5. Fill in the placeholder on the About page with the company story and team.

## What's left off on purpose

These features aren't live in the app yet, so the site doesn't mention them:

- Assets
- Performance
- Access/ID cards
- Attendance
- Recruitment
- GOSI/WPS automation
- Third-party integrations
- Arabic

## Research

`research/` holds the competitor analysis and the page plan. `robots.txt` asks search engines not to index it.
