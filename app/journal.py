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
        Link(rel="icon", type="image/x-icon", href="/static/favicon.ico"),
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
                cursor: pointer;
            }
            .dot.selected {
                background-color: #007BFF;
            }
            #new-entry-form-section {
                margin-top: 20px;
            }
            /* Entry View */
            #entry-view {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                padding: 20px;
                margin: 10px 0;
                width: 100%; /* Make it full width */
                max-width: 100%; /* Ensure it doesn't overflow */
                box-sizing: border-box; /* Include padding and border in the width */
             }

            """)
    ),
)

def heading():
    
    new_entry_div = DivRAligned(Button(
                UkIcon('plus', height=17, width=17),
                " New Entry ",
                cls=ButtonT.primary,
                hx_get="/show_new_entry_form",
                hx_target="#new-entry-form-section",
                hx_swap="beforeend",
                id="show_entry_button"
            ))
    

    return Div(cls=(FlexT.between, FlexT.middle))(
        H2("Journal"), new_entry_div,
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

def generate_month_list(start_year_month=(1905, 1)):
    """
    Generates a list of (year, month) tuples from a given start date to the present day.

    Args:
        start_year_month (tuple): A tuple in the format (start_year, start_month).

    Returns:
        list: A list of tuples, where each tuple is (year, month).
    """
    start_year, start_month = start_year_month
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


@rt("/show_entry/{date_str}")
def show_entry(date_str: str):
    """Shows the details of journal entries for a specific date."""
    entries = load_journal_entries()
    entries_for_date = [e for e in entries if e["date"] == date_str]

    # Ensure the container always exists
    entry_view = Div(
        id="entry-view",
        cls="relative border p-4 bg-white shadow-md rounded-md w-fit mx-auto mt-4", hidden=False
    )

    # Close button
    close_button = Button(
        "❌",
        cls="absolute top-1 right-1 text-white text-sm rounded-full bg-red-500 hover:bg-red-600 p-1 w-6 h-6 flex items-center justify-center cursor-pointer",
        hx_get="/close-entry",  # Calls the route to clear content
        hx_target="#entry-view",  # Ensures only this div is emptied
        hx_swap="outerHTML"  # Clears the content instead of removing the div
    )

    if not entries_for_date:
        entry_view(
            Div("No entries found for this date", cls="p-2 text-gray-500"),
            close_button
        )
    else:
        for entry in entries_for_date:
            entry_view(
                Div(
                    close_button,
                    Div(entry["date"], cls=(TextT.bold, "mb-2")),
                    Div(entry["entry"], cls="whitespace-pre-wrap"),
                )
            )

    return entry_view

@rt("/close-entry")
def close_entry():
    return Div(id="entry-view", hidden=True)  # Leaves an empty, hidden div in place


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
    entries = load_journal_entries()
    entry_dates = {entry["date"] for entry in entries}

    # Determine the earliest entry date
    if entries:
        earliest_date_str = min(entry_dates)
        earliest_date = datetime.fromisoformat(earliest_date_str).date()
        start_year_month = (earliest_date.year, earliest_date.month)
    else:
        start_year_month = (1905,1)

    month_list = generate_month_list(start_year_month)

    grid = DivVStacked(cls="w-full gap-1 align-start")

    for year_month in month_list:
        year, month = year_month
        days = generate_days_in_month(year_month)
        month_year_label = Div(f"{calendar.month_abbr[month]} {year}", cls="month-year")
        dots = Div(cls="dots")
        for day in days:
            date_str = f"{year}-{month:02}-{day:02}"
            dot_cls = "dot selected" if date_str in entry_dates else "dot"
            dot_attrs = {"cls": dot_cls}
            if date_str in entry_dates:
                dot_attrs.update({
                    "hx_get": f"/show_entry/{date_str}",
                    "hx_target": "#entry-view",
                    "hx_swap": "outerHTML",
                    "hx_trigger": "click",
                    "hx_indicator":".htmx-indicator"
                })
            dots(Div(**dot_attrs))
        grid(Div(month_year_label, dots, cls='entry'))

    return grid

def listView():
    entries = load_journal_entries()
    #filter out any incorrect values
    valid_entries = []
    for entry in entries:
        if "date" not in entry:
             continue
        if not isinstance(entry.get('date'), str):
            print(f"Skipping entry with invalid date type: {entry}")
            continue
        try:
            date.fromisoformat(entry["date"])
            valid_entries.append(entry)
        except (ValueError, TypeError):
            print(f"Skipping invalid entry: {entry}")

    # Sort entries by date (newest first)
    valid_entries.sort(key=lambda x: date.fromisoformat(x['date']) , reverse=True)

    list_view = DivVStacked(cls="w-full gap-1 align-start")

    # Define table headers
    headers = ["Date", "Entry"]

    # Convert the valid entries into table row format
    body_data = [[entry["date"], entry["entry"]] for entry in valid_entries]

    # Create the table
    list_view(
        TableFromLists(
            header_data=headers,
            body_data=body_data,
            cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm),
            sortable=True
        )
    )


    return list_view

def view_content():
    return Div(id="view-container")(
        Div(id="entry-view", hidden=True), 
        Ul(id="component-nav", cls="uk-switcher")(
                Li(dayGrid()), #grid view
                Li(listView()) #list view
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
            view_content(),
            Div(
                Img(
                    src="/spin.svg",
                    cls="htmx-indicator",
                    style="width:2rem",
                ),
                style="display:none"
            )
        )
    )

serve(port=7127)
