# MyJournal - A Simple Journaling Application

MyJournal is a lightweight web application that allows you to keep track of your daily thoughts and experiences in a simple and organized manner. It offers two primary views: a grid view that visually represents your entries by date, and a list view for quickly browsing through your journal entries.

## Features

-   **Journal Entry Creation:** Easily create new journal entries with a date and text content.
-   **Date-Based Organization:** Entries are automatically organized by date.
-   **Grid View:** Visualize your journal entries in a calendar-like grid, with each day represented by a circle. Days with entries are highlighted.
-   **List View:** Browse through your entries in a chronological list format, with the newest entries at the top.
-   **Persistent Storage:** Journal entries are saved to a JSON file (`journal_entries.json`) on your local machine, ensuring your data persists across sessions.
- **Input Validation:** The application validates the date format of your entries to avoid saving invalid data.
- **Clear UI:** Simple and clean design, leveraging UIkit, MonsterUI, and Fasthtml.
- **HTMX powered:** leverages HTMX for a smooth single page app experience.

## Technologies Used

-   **Python:** The core programming language.
-   **Fasthtml:** A framework for building web applications quickly using Python.
-   **MonsterUI:** A UI library for styling and component management.
-   **UIkit:** A lightweight and modular front-end framework for developing web interfaces.
- **HTMX:** Provides the smooth single page app experience.
-   **JSON:** For storing journal entries in a structured format.

## Installation and Setup

1.  **Prerequisites:**
    -   Python 3.x installed on your system.
    -   `pip` (Python package installer)

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    *Note:* Create `requirements.txt` with the following:

    ```
    fasthtml
    monsterui
    ```

3.  **Run the Application:**
    ```bash
    python app/journal.py
    ```

4.  **Access the Application:**
    Open your web browser and go to `http://localhost:7127/`.

## Usage

1.  **Creating a New Entry:**
    -   Click the "New Entry" button.
    -   Select the date for your entry using the date picker.
    -   Write your journal entry in the text area.
    -   Click "Save" to save the entry.
    - Alternatively you can press "Cancel" to cancel and close the form

2.  **Navigating Views:**
    -   Click "Grid View" to view entries in a grid layout.
    -   Click "List View" to view entries in a list layout.

3.  **Data Storage:**
    -   All entries are stored in the `journal_entries.json` file.

## How it Works

The application uses Fasthtml to handle web requests and render the user interface. MonsterUI and UIkit provide styling and pre-built UI components.

- **`journal.py`**:
  - Defines the application logic, including handling journal entry creation, saving, loading, and rendering views.
  - Defines the HTMX endpoints.
  - Defines `dayGrid` and `listView` functions for the main views.
  - Uses the `JournalEntry` dataclass to structure entry data.
  - Generates dynamic HTML with Fasthtml.

-   **JSON File (`journal_entries.json`):**
    -   This file stores the journal entries as a JSON array. Each entry has:
        -   `id`: A unique identifier.
        -   `date`: The date of the entry in ISO format (e.g., "2023-10-27").
        -   `entry`: The text content of the entry.
        - `timestamp`: when the entry was saved

- **HTMX**
  - Handles the smooth single page app experience

## Future Enhancements

-   **Entry Editing:** Allow users to edit existing entries.
-   **Entry Deletion:** Add the ability to delete entries.
-   **Search Functionality:** Implement a search feature to easily find specific entries.
-   **User Authentication:** Add user login and separate journals for different users.
- **Tagging:** Add the ability to add tags to journal entries.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.
