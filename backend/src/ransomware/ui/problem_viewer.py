from pathlib import Path
import tkinter as tk

from tkinterweb import HtmlFrame

from ransomware.config import VIEWER_MISSING_TEXT, VIEWER_WINDOW_SIZE
from ransomware.ui.styles import BG_PRIMARY


class ProblemViewer(tk.Toplevel):
    """Spawns a styled Toplevel window and renders the problem HTML via HtmlFrame."""

    def __init__(self, parent: tk.Tk, problem_id: str, problems_path: Path):
        super().__init__(parent)
        self.title(f"Problem {problem_id.upper()}")
        self.geometry(VIEWER_WINDOW_SIZE)
        self.configure(bg=BG_PRIMARY)
        self.resizable(True, True)

        html = HtmlFrame(self, messages_enabled=False)
        html.pack(fill="both", expand=True)

        problem_file = problems_path / f"{problem_id}.html"
        if problem_file.exists():
            html.load_file(str(problem_file))
        else:
            html.load_html(VIEWER_MISSING_TEXT)
