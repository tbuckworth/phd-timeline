#!/usr/bin/env python3

"""
generate_chart.py
===================

This script produces a simple Gantt‑style timeline plot for a PhD project.  It
defines a set of events (internships, funding periods, teaching duties,
conference dates and paper submission goals) and draws horizontal bars for each
on a shared calendar axis.  The output is saved as ``timeline.png`` in the
current directory.

To modify the schedule, edit the ``events`` list below.  Each entry is a
tuple ``("label", start_date, end_date)`` where ``start_date`` and
``end_date`` are ``datetime.date`` objects.  Single‑day events can be
represented by using the same start and end date.

Example:

    ("New experiment", date(2026, 3, 1), date(2026, 3, 15))

This plot makes use of matplotlib only – there are no external dependencies
besides Python's standard library.  The colours and figure size can be
customised as needed.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from typing import List, Tuple


def build_events() -> List[Tuple[str, date, date]]:
    """Return a list of timeline entries.

    The entries below reflect the user’s current PhD timeline.  Modify or
    extend this list as your plans evolve.  See the docstring at the top of
    this file for guidance on the expected tuple format.
    """
    # Today’s date is used to anchor the internship start point.  Adjust
    # accordingly if your internship started earlier.
    today = date.today()

    return [
        ("Internship at Epic", today, date(2025, 12, 31)),
        ("Funding (18 months)", date(2026, 1, 1), date(2027, 6, 30)),
        ("Unfunded period", date(2027, 7, 1), date(2027, 12, 31)),
        ("Teaching duties", date(2026, 1, 1), date(2026, 12, 31)),
        # Major machine learning conferences.  The dates for AAAI and ICML vary
        # from year to year; the ranges here use typical windows from recent
        # editions (AAAI late February/early March, ICML mid‑July and NeurIPS
        # early December).  Adjust as new dates are announced.
        ("NeurIPS 2025", date(2025, 12, 2), date(2025, 12, 7)),
        ("AAAI 2026", date(2026, 1, 20), date(2026, 1, 27)),
        ("ICML 2026", date(2026, 7, 13), date(2026, 7, 19)),
        ("NeurIPS 2026", date(2026, 12, 1), date(2026, 12, 7)),
        ("AAAI 2027", date(2027, 2, 1), date(2027, 2, 8)),
        ("ICML 2027", date(2027, 7, 10), date(2027, 7, 16)),
        ("NeurIPS 2027", date(2027, 12, 1), date(2027, 12, 7)),
        # Paper submission goals.  These are one‑day events and can be moved
        # easily.  PIRC submission is aimed at NeurIPS (abstract deadlines
        # typically fall in May).  The second paper is targeted at AAAI.
        ("PIRC submission", date(2026, 5, 16), date(2026, 5, 16)),
        ("Second paper submission", date(2027, 8, 15), date(2027, 8, 15)),
    ]


def create_timeline(events: List[Tuple[str, date, date]], output_path: str) -> None:
    """Draw a Gantt‑style chart and save it to ``output_path``.

    Args:
        events: A list of (label, start, end) tuples.
        output_path: Path to the image file to be created.
    """
    # Sort events by start date to ensure sensible ordering on the plot
    events_sorted = sorted(events, key=lambda item: item[1])
    labels = [event[0] for event in events_sorted]
    starts = [mdates.date2num(event[1]) for event in events_sorted]
    ends = [mdates.date2num(event[2]) for event in events_sorted]
    durations = [end - start for start, end in zip(starts, ends)]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bars – each at y‑position i.  Use a consistent colour map for
    # readability.  Single‑day events will result in very narrow bars.
    cmap = plt.cm.get_cmap("tab20")
    for i, (label, start, duration) in enumerate(zip(labels, starts, durations)):
        colour = cmap(i % cmap.N)
        ax.barh(i, duration if duration > 0 else 0.1, left=start, height=0.5,
                color=colour, edgecolor='k')

    # Set y‑axis labels and ticks
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # so the earliest event appears at the top

    # Format the x‑axis to show months and years
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.autofmt_xdate()

    # Add grid for visual clarity
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.set_title('PhD Timeline Overview')
    ax.set_xlabel('Date')

    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


if __name__ == '__main__':
    timeline_events = build_events()
    create_timeline(timeline_events, 'timeline.png')