# Scholarship Eligibility Checker (extension)

## Try it
1. Open `edge://extensions` or `chrome://extensions`.
2. Turn on **Developer mode**, click **Load unpacked**, select this `extension/` folder.
3. Click the extension icon → **Edit my profile**, fill it in, save.
4. Go to any scholarship page, click the icon, click **Check this page**.

It uses fake (mock) results until the backend is ready.

## Connecting the real backend
In `config.js`, set `USE_MOCK: false` and make sure `API_URL` points at the backend.
After any file change, click the reload icon on the extension card.

## Files
- `manifest.json` – extension settings and permissions
- `config.js` – mock switch and backend URL
- `api.js` – calls the backend (see `../docs/api-contract.md`)
- `compare.js` – eligibility rules (plain code, no AI)
- `popup.html/js` – what appears when you click the icon
- `options.html/js` – profile settings page
- `styles.css` – shared styles
