from fasthtml.common import *
from monsterui.all import *
from datetime import date, datetime
import calendar
import json
import uuid
import os
from dataclasses import dataclass

JOURNAL_ENTRIES_FILE = "data/journal_entries.json"

@dataclass
class JournalEntry:
    entry_date: str
    entry_text: str

app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(
        *Theme.blue.headers(highlightjs=True),
        Link(rel="icon", type="image/x-icon", href="/favicon.ico"),
        SortableJS(".sortable"),
        Style("""
            body {
                font-family: sans-serif;
                margin: 2rem;
                background-color: #f9f9f9;
            }

            /* Header */
            header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 1.5rem;
            }
            header h1 {
                font-size: 1.2rem;
                margin: 0;
            }
            .header-buttons button {
                margin-left: 0.5rem;
                padding: 0.5rem 1rem;
                border: none;
                background-color: #007BFF;
                color: #fff;
                cursor: pointer;
                border-radius: 4px;
            }

            .journal-list {
                display: flex;
                flex-direction: column;
                gap: 0.2rem;
                align-items: flex-start;
                width: 100%;
            }
            .entry {
                display: flex;
                align-items: flex-start;
                margin-bottom: 0.1rem;
                width: 100%;
            }
            .month-year {
                width: 6rem;
                font-weight: 500;
                text-align: left;
                font-size: 0.9rem;
            }

            /* Dot row */
            .dots {
                display: flex;
                flex-wrap: wrap;
                gap: 0.3rem;
                align-items:flex-start;
            }
            .dot {
                width: 12px;
                height: 12px;
                border-radius: 2px;
                background-color: #ccc;
            }
            .dot.selected {
                background-color: #007BFF;
            }
            #new-entry-form-section {
                margin-top: 20px;
            }
            .list-entry {
              border-bottom: 1px solid #ccc;
              padding: 10px 0;
            }
            .list-entry .date {
              font-weight: bold;
            }
        """)
    ),
)

def heading():
    return Div(
        H2("Journal"),
        Div(
            Button(
                UkIcon('plus', height=17, width=17),
                " New Entry ",
                cls=ButtonT.primary,
                hx_get="/show_new_entry_form",
                hx_target="#new-entry-form-section",
                hx_swap="beforeend",
                id="show_entry_button"
            ),          
            cls="flex gap-x-2 items-center"
        ),
        cls="flex justify-between items-center",
        id="heading-container"
    )

@rt("/show_new_entry_form")
def show_new_entry_form():
    """Returns the form content."""
    return Div(
        Form(
            Div(
                Input(
                    type="date",
                    name="entry_date",
                    cls="uk-input border border-gray-300 px-2 py-1 rounded w-full",
                    aria_label="Date",
                    title="Date"
                ),
                TextArea(
                    name="entry_text",
                    placeholder="Write your entry here...",
                    rows="5",
                    cls="uk-textarea border border-gray-300 p-2 rounded w-full",
                    aria_label="Journal Entry",
                    title="Journal Entry"
                ),
                cls="space-y-4",
            ),
            Div(
                Button("Cancel", cls=ButtonT.secondary, type="button", hx_get="/hide_form", hx_target="#new-entry-form-section",hx_swap="outerHTML"),
                Button("Save", cls=ButtonT.primary, type="submit")
                ),

            name="new-entry-form",
            hx_post="/save_entry",
            hx_target="#new-entry-form-section",
            hx_swap="outerHTML",
        ),
        id="form-content"
    )

@rt("/hide_form")
def hide_form():
    """Hides the form and clears its contents."""
    return Div(id="form-content")

@rt("/save_entry")
def save_entry(entry: JournalEntry): #use entry: JournalEntry
    """Handles saving journal entries to a JSON file."""
    entry_date = entry.entry_date #get data from entry
    entry_text = entry.entry_text #get data from entry

    #validate date
    try:
        datetime.fromisoformat(entry_date)
    except ValueError:
        print(f"invalid date: {entry_date}. Skipping entry")
        return Div(id="form-content")

    new_entry = {
        "id": str(uuid.uuid4()),  # Generate a unique ID
        "date": entry_date,
        "entry": entry_text,
        "timestamp": datetime.now().isoformat(),  # Add a timestamp
    }

    # Load existing entries or create an empty list
    try:
        with open(JOURNAL_ENTRIES_FILE, "r") as f:
            entries = json.load(f)
    except FileNotFoundError:
        entries = []

    # Add the new entry and save back to the file
    entries.append(new_entry)
    with open(JOURNAL_ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=4)
    return Div(id="form-content") #return blank div!

def load_journal_entries():
    """Loads journal entries from the JSON file."""
    try:
        with open(JOURNAL_ENTRIES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_month_list():
    """
    Generates a list of (year, month) tuples for every month from January 1905 to the present day.

    Returns:
        list: A list of tuples, where each tuple is (year, month).
    """
    start_year = 1905
    start_month = 1
    today = date.today()
    current_year = today.year
    current_month = today.month

    month_list = []
    year = start_year
    month = start_month

    while year < current_year or (year == current_year and month <= current_month):
        month_list.append((year, month))
        month += 1
        if month > 12:
            month = 1
            year += 1

    return month_list


def generate_days_in_month(year_month: tuple) -> list:
    """
    Generates a list of days (integers) for a given month and year.

    Args:
        year_month (tuple): A tuple in the format (year, month), where year is an integer and month is an integer (1-12).

    Returns:
        list: A list of integers representing the days in the specified month.
              Returns an empty list if the input is invalid.
    """
    try:
        year, month = year_month
        # Validate year and month
        if not isinstance(year, int) or not isinstance(month, int):
            raise ValueError("Year and month must be integers.")
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")

        # Get the number of days in the specified month
        _, num_days = calendar.monthrange(year, month)

        # Create the list of days
        days_list = list(range(1, num_days + 1))
        return days_list

    except ValueError as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error
    except TypeError:
        print(f"Error: Invalid Input type, must be tuple of (year, month).")
        return []  # Return an empty list on error


def dayGrid():
    """
    Generates a DivVStacked grid where each row represents a year_month
    and within each row there are small circles, one for each value from generate_days_in_mont.
    Colors days with existing entries.

    Args:
        none
    Returns:
        returns a DivVStacked object
    """
    month_list = generate_month_list()
    entries = load_journal_entries()
    entry_dates = {entry["date"] for entry in entries}

    grid = DivVStacked(cls="journal-list")

    for year_month in month_list:
        year, month = year_month
        days = generate_days_in_month(year_month)
        month_year_label = Div(f"{calendar.month_abbr[month]} {year}", cls="month-year")
        dots = Div(cls="dots")
        for day in days:
            date_str = f"{year}-{month:02}-{day:02}"
            dot_cls = "dot selected" if date_str in entry_dates else "dot"
            dots(Div(cls=dot_cls))
        grid(Div(month_year_label, dots, cls='entry'))

    return grid

def listView():
    entries = load_journal_entries()
    #filter out any incorrect values
    valid_entries = []
    for entry in entries:
        if "date" not in entry:
             print(f"Skipping entry with missing date: {entry}")
             continue
        if not isinstance(entry.get('date'), str):
            print(f"Skipping entry with invalid date type: {entry}")
            continue

        try:
            datetime.fromisoformat(entry["date"])
            valid_entries.append(entry)
        except (ValueError, TypeError):
            print(f"Skipping invalid entry: {entry}")

    # Sort entries by date (newest first)
    valid_entries.sort(key=lambda x: datetime.fromisoformat(x['date']) , reverse=True)

    list_view = Div(cls="journal-list")
    for entry in valid_entries:
        list_view(Div(Div(entry['date'], cls="date"), Div(entry["entry"]), cls="list-entry"))
    return list_view

def view_content():
    return Div(id="view-container")(
        Ul(id="component-nav", cls="uk-switcher")(
                Li(dayGrid()),
                Li(listView())
        )
    )

@rt("/")
def index(request=None):
    return view(request)

def view(request=None):
    tabs = TabContainer(
        Li(A('Grid View',    href='#'),    cls='uk-active'),
        Li(A('List View', href='#')),
        uk_switcher='connect: #component-nav; animation: uk-animation-fade',
        alt=True
    )

    return Header(
        Title("Forms Example"),
        Container(
            heading(),
            Div(tabs),
            Div(id="new-entry-form-section"),
            view_content()
        )
    )

serve(port=7127)