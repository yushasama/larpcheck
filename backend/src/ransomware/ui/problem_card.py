from dataclasses import dataclass
from typing import Callable
import tkinter as tk

from ransomware.config import (
    CARD_BUTTON_WIDTH,
    DROP_WRAP_LENGTH,
    DROP_FILE_TEXT,
    OPEN_PROBLEM_TEXT,
    PANEL_PAD_X,
    PANEL_PAD_Y,
    SELECT_FILE_TEXT,
    STATUS_PENDING_TEXT,
    SUBMIT_TEXT,
    TITLE_WRAP_LENGTH,
)
from ransomware.ui.styles import (
    BG_CARD,
    BG_DARK,
    BG_DROP,
    BG_PRIMARY,
    FG_ACCENT,
    FG_DIM,
    FG_ORANGE,
    FONT_MONO,
    FONT_MONO_BOLD,
)


@dataclass
class ProblemCard:
    problem_id: str
    problem_num: int
    file_path: str | None
    status_label: tk.Label
    submit_btn: tk.Button
    drop_label: tk.Label


def build_problem_card(
    parent: tk.Frame,
    num: int,
    pid: str,
    title: str,
    problem_id: str,
    on_select: Callable,
    on_submit: Callable,
    on_open: Callable,
) -> ProblemCard:
    card = tk.Frame(parent, bg=BG_CARD, bd=1, highlightthickness=1, highlightbackground=FG_DIM)
    card.pack(fill="x", padx=PANEL_PAD_X, pady=PANEL_PAD_Y)

    title_label = tk.Label(
        card,
        text=f"Problem {pid.upper()} [{num}]  {title}",
        bg=BG_CARD,
        fg=FG_ACCENT,
        font=FONT_MONO_BOLD,
        anchor="w",
        justify="left",
        wraplength=TITLE_WRAP_LENGTH,
    )
    title_label.pack(fill="x", padx=PANEL_PAD_X, pady=(PANEL_PAD_Y, 0))

    controls = tk.Frame(card, bg=BG_CARD)
    controls.pack(fill="x", padx=PANEL_PAD_X, pady=PANEL_PAD_Y)

    select_btn = tk.Button(
        controls,
        text=SELECT_FILE_TEXT,
        width=CARD_BUTTON_WIDTH,
        command=lambda: on_select(problem_id),
        bg=BG_DARK,
        fg=FG_ORANGE,
        activebackground=BG_PRIMARY,
        activeforeground=FG_ACCENT,
        relief="flat",
        font=FONT_MONO,
    )
    select_btn.pack(side="left")

    open_btn = tk.Button(
        controls,
        text=OPEN_PROBLEM_TEXT,
        width=CARD_BUTTON_WIDTH,
        command=lambda: on_open(problem_id),
        bg=BG_DARK,
        fg=FG_ORANGE,
        activebackground=BG_PRIMARY,
        activeforeground=FG_ACCENT,
        relief="flat",
        font=FONT_MONO,
    )
    open_btn.pack(side="left", padx=PANEL_PAD_X)

    submit_btn = tk.Button(
        controls,
        text=SUBMIT_TEXT,
        width=CARD_BUTTON_WIDTH,
        command=lambda: on_submit(problem_id),
        bg=BG_DARK,
        fg=FG_ORANGE,
        activebackground=BG_PRIMARY,
        activeforeground=FG_ACCENT,
        relief="flat",
        font=FONT_MONO,
    )
    submit_btn.pack(side="left")

    status_label = tk.Label(
        controls,
        text=STATUS_PENDING_TEXT,
        bg=BG_CARD,
        fg=FG_ORANGE,
        font=FONT_MONO_BOLD,
        anchor="e",
    )
    status_label.pack(side="right")

    drop_label = tk.Label(
        card,
        text=DROP_FILE_TEXT,
        bg=BG_DROP,
        fg=FG_DIM,
        font=FONT_MONO,
        anchor="w",
        justify="left",
        wraplength=DROP_WRAP_LENGTH,
    )
    drop_label.pack(fill="x", padx=PANEL_PAD_X, pady=(0, PANEL_PAD_Y))

    return ProblemCard(
        problem_id=problem_id,
        problem_num=num,
        file_path=None,
        status_label=status_label,
        submit_btn=submit_btn,
        drop_label=drop_label,
    )
