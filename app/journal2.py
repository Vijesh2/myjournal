import uvicorn
import json
from datetime import datetime
from pathlib import Path
# This wildcard import should bring in FT
from fasthtml.common import *
# We need Union for the type hint if using Python < 3.10
from typing import Union

# --- Configuration ---
DATA_FILE = Path("journal_entries.json")

# --- Data Handling ---
# (load_entries and save_entries remain the same)
def load_entries():
    """Loads journal entries from the JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading entries: {e}")
        return []

def save_entries(entries):
    """Saves journal entries to the JSON file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving entries: {e}")


# --- Application Setup ---
app = FastHTML()
rt = app.route # Define routes using the @rt decorator

# Load initial entries when the app starts
journal_entries = load_entries()

# --- UI Components ---

# Corrected type hint using FT (Option 1: Python 3.10+)
# def layout(content: FT | list[FT]):

# Corrected type hint using FT (Option 2: Python < 3.10 or broader compatibility)
def layout(content: Union[FT, list[FT]]):
    """Basic page layout using PicoCSS."""
    # Ensure content is always a list for unpacking
    if not isinstance(content, (list, tuple)):
        content = [content]
    return Titled("Simple Journal",
        Main(cls="container", *content), # Unpack the content list
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
        Link(rel="stylesheet", href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css")
    )

# (entry_display, journal_list_component, add_entry_form remain the same)
def entry_display(entry: dict):
    """Renders a single journal entry."""
    timestamp = entry.get("timestamp", "No date")
    content = entry.get("content", "No content")
    return Article(
        Header(Small(timestamp)),
        P(content),
        style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--muted-border-color);"
    )

def journal_list_component(entries: list):
    """Renders the list of journal entries."""
    if not entries:
        return P("No journal entries yet.")
    return Div(*[entry_display(entry) for entry in reversed(entries)], id="entries-list")

def add_entry_form():
    """Renders the form to add a new entry."""
    return Form(
        H3("Add New Entry"),
        Textarea(name="content", placeholder="Write your thoughts...", required=""),
        Button("Add Entry", type="submit"),
        hx_post="/add",
        hx_target="#entries-list",
        hx_swap="outerHTML",
        hx_on__htmx_after_request="this.reset()"
    )


# --- Routes ---
@rt("/")
async def get():
    """Serves the main page."""
    # Pass the components as a list to layout
    return layout([
        journal_list_component(journal_entries),
        add_entry_form()
    ])

# (post_add remains the same)
@rt("/add")
async def post_add(content: str):
    """Handles adding a new entry."""
    if not content or not content.strip():
        return journal_list_component(journal_entries)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {"timestamp": now, "content": content.strip()}

    journal_entries.append(new_entry)
    save_entries(journal_entries)

    return journal_list_component(journal_entries)


# --- Run ---
# (if __name__ == "__main__": block remains the same)
if __name__ == "__main__":
    if not DATA_FILE.exists():
        save_entries([])
    uvicorn.run(app, host="0.0.0.0", port=8000)