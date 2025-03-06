# My Journal App 📝

A simple web-based journal application to keep track of your daily thoughts and activities.

## Features ✨

*   **Create New Entries:** Easily add new journal entries with a date and text content. 🖋️
*   **Date Validation:** Ensures that entered dates are valid. ✅
*   **Persistent Storage:** Saves journal entries to a `journal_entries.json` file in the `data` folder, so your entries are preserved across sessions. 💾
*   **Unique IDs:** Each entry has a unique ID for easy identification.
*   **Timestamping:** Entries are automatically timestamped with their creation time. 🕰️
*   **Grid View:** Visualize your journal entries in a calendar-like grid view. 📅
*   **List View:** See your entries in a chronological list format. 📜
*   **Tabs:** Toggle between grid and list views with easy navigation.
*   **Dynamic Updates:** Uses HTMX (implicit in the code, due to `hx_*` attributes) for a smooth, dynamic user experience without full-page reloads.
*   **Clean UI:** Uses MonsterUI for good looking components.
*   **Responsive Design:** Uses uk- classes for a good look on both large and mobile screens.

## Installation and Setup 🚀

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd myjournal
    ```

2.  **Create a virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate #linux/MacOS
    .venv\Scripts\activate #Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    ```bash
    python app/journal.py
    ```
    The application will be available at `http://localhost:7127`.

## File Structure 📁

```bash
myjournal/
├── app/
│   └── journal.py           # Main application code
├── data/
│   └── journal_entries.json # Stores your journal entries (will be created automatically)
├── .gitignore               # Specifies which files to ignore
├── requirements.txt         # List of Python dependencies
└── README.md                # This file explains the project
```

## How to Use 🤔

1.  **New Entry:** Click the "New Entry" button to open the entry form.
2.  **Fill Form:** Enter the date and your journal entry in the provided fields.
3.  **Save:** Click "Save" to save the entry. The form will automatically close.
4.  **Cancel:** Click "Cancel" to close the form without saving.
5.  **Grid view:** Navigate to the grid view to see all the days with an entry.
6.  **List View:** navigate to the list view to see all the entries as a list.

## Technologies Used 🛠️

*   **Python:** The core programming language.
*   **Fasthtml:**  For creating the web application efficiently.
*   **MonsterUI:** A component library used to make the user interface look good.
*   **HTMX:** (Implied) For dynamic updates of the UI without full page reloads.
*   **`uuid`:** For generating unique IDs for journal entries.
*   **`datetime`:** For handling dates and timestamps.
*   **`json`:** For saving and loading journal entries.
*   **Calendar:** Used to generate months and days.
*   **`dataclasses`:** for data classes.

## Contributing 🤝

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

## License 📄

[MIT License]
