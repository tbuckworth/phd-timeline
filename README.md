# PhD Timeline Chart

This repository generates a simple timeline chart to visualise your PhD
milestones.  It uses Python and matplotlib to draw a horizontal Gantt‑style
chart showing the end of your internship, funded and unfunded periods,
teaching duties, key machine learning conference windows and paper submission
goals.  A weekly GitHub Action runs the script, regenerates the chart and
emails it to you as a reminder.

## Contents

- **generate_chart.py** – builds the timeline and writes `timeline.png`.
- **send_email.py** – sends the generated image via email using SMTP.
- **requirements.txt** – lists Python dependencies (matplotlib).
- **.github/workflows/weekly_email.yml** – GitHub Action that runs weekly to
  regenerate the chart and send it to you.

## Editing the schedule

Open `generate_chart.py` and locate the `build_events()` function.  Each event
is defined by a label and a start/end date:

```python
('Internship at Epic', date(2025, 8, 7), date(2025, 12, 31))
```

To modify dates or add new milestones, edit this list accordingly.  Single‑day
events (such as a submission deadline) should use the same start and end date.

After editing, run the script locally to generate a new chart:

```bash
python3 generate_chart.py
```

The PNG image will be saved as `timeline.png` in the repository root.

## Email configuration

The `send_email.py` script uses standard SMTP over SSL.  You must supply your
email address and password as environment variables when running the script.
For example:

```bash
export EMAIL_ADDRESS="your.email@example.com"
export EMAIL_PASSWORD="your‑app‑specific‑password"
python3 send_email.py
```

If `RECIPIENT_EMAIL` is unset, the message will be sent to the sender
(`EMAIL_ADDRESS`).  Gmail users will likely need to generate an app‑specific
password to use with SMTP and may need to enable “less secure apps” in their
account settings.

## GitHub Actions

The workflow defined in `.github/workflows/weekly_email.yml` runs once a week
(Monday at 08:00 UTC) and whenever you manually dispatch it.  It installs
dependencies, generates the timeline and emails the result via `send_email.py`.
The secrets required to authenticate with your mail provider must be added
under the repository’s *Settings → Secrets and variables*:

- `EMAIL_ADDRESS` – your email account
- `EMAIL_PASSWORD` – an app‑specific or normal password
- `RECIPIENT_EMAIL` – where to send the report (optional; defaults to
  `EMAIL_ADDRESS`)
- optionally `SMTP_SERVER` and `SMTP_PORT` if you aren’t using Gmail

Once these secrets are configured, the workflow will automatically email you
the updated chart every week.  You can also trigger the workflow on demand
via the “Run workflow” button on the Actions page.

## Local development

To set up the project on your machine:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 generate_chart.py
```

This will create `timeline.png`.  You can then run `send_email.py` as shown
above to send the chart manually.

## Attribution

The conference timing information is based on typical dates from recent
editions.  For example, NeurIPS is held every December【529939245562218†L139-L145】,
ICML 2025 runs from 13–19 July【697297052701205†L240-L247】, and AAAI’s 2025 meeting
took place from 25 February to 4 March【911908019878943†L89-L96】 while the 2026 edition
was scheduled for 20–27 January【865790923874874†L93-L96】.  Adjust the dates in
`generate_chart.py` as necessary when new conference schedules are released.