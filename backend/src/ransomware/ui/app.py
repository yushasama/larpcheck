from pathlib import Path
import random
import shutil
import time
import tkinter as tk
from tkinter import filedialog

from judge.judge import judge_submission
from ransomware.config import (
    ACTIVE_PROBLEM_COUNT,
    BODY_TEXT,
    DEADLINE_LABEL_TEXT,
    DEADLINE_SECONDS,
    END_TIMER_TEXT,
    HEADER_TEXT,
    PANEL_PAD_X,
    PANEL_PAD_Y,
    PENALTY_SECONDS,
    PROBLEM_COUNT_TO_DECRYPT,
    PROBLEM_IDS,
    PROBLEM_TITLES,
    PROBLEMS_PATH,
    RESET_TEXT,
    SANDBOX_PATH,
    SANDBOX_BACKUP_PATH,
    STATUS_NO_BACKUP_TEXT,
    STATUS_COMPILE_ERROR_TEXT,
    STATUS_DECRYPTED_TEXT,
    STATUS_DROPPED_TEXT,
    STATUS_ENCRYPTED_TEXT,
    STATUS_ERROR_TEXT,
    STATUS_INVALID_DROP_TEXT,
    STATUS_NO_FILE_TEXT,
    STATUS_PENDING_TEXT,
    STATUS_RUNTIME_ERROR_TEXT,
    STATUS_RESET_TEXT,
    STATUS_ROUND_ENDED_TEXT,
    STATUS_SANDBOX_RESTORED_TEXT,
    STATUS_SEGFAULT_TEXT,
    STATUS_SOLVED_TEXT,
    STATUS_TLE_TEXT,
    STATUS_WRONG_TEXT,
    SUCCESS_BODY_TEXT,
    SUCCESS_HEADER_TEXT,
    TIMER_TICK_MS,
    TITLE_TEXT,
    WINDOW_SIZE,
)
from ransomware.countdown import Countdown
from ransomware.crypto import decrypt_all, encrypt_all
from ransomware.state import RansomwareState, clear_state, load_state, save_state
from ransomware.ui.problem_card import ProblemCard, build_problem_card
from ransomware.ui.problem_viewer import ProblemViewer
from ransomware.ui.styles import (
    BG_DARK,
    BG_PRIMARY,
    FG_ACCENT,
    FG_DIM,
    FG_ERROR,
    FG_SOLVED,
    FG_TIMER,
    FONT_DEADLINE,
    FONT_MONO,
    FONT_MONO_BOLD,
    FONT_TITLE,
)

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None


class LarpCheckUI:
    def __init__(self) -> None:
        self.root = TkinterDnD.Tk() if TkinterDnD is not None else tk.Tk()
        self.root.title(TITLE_TEXT)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.state = load_state()
        if len(self.state.active_problem_ids) != ACTIVE_PROBLEM_COUNT:
            self.state.active_problem_ids = random.sample(PROBLEM_IDS, k=ACTIVE_PROBLEM_COUNT)
            self.state.solved_problem_ids = []
            save_state(self.state)

        self.countdown = Countdown(DEADLINE_SECONDS, started_at=self.state.started_at)
        self.cards: list[ProblemCard] = []
        self.cards_container: tk.Frame | None = None
        self.viewer_by_problem: dict[str, ProblemViewer] = {}
        self.solved_problem_ids: set[str] = set(self.state.solved_problem_ids)
        self.active_problem_ids = list(self.state.active_problem_ids)
        self.persist_on_close = True

        self.deadline_label: tk.Label | None = None
        self.banner_label: tk.Label | None = None
        self.subtitle_label: tk.Label | None = None
        self.description_label: tk.Label | None = None

        self.ensure_sandbox_seeded()
        self.build_layout()
        if self.state.round_active:
            self.encrypt_sandbox()
        self.refresh_timers()

    def build_layout(self) -> None:
        header = tk.Frame(self.root, bg=BG_PRIMARY)
        header.pack(fill="x", padx=PANEL_PAD_X, pady=PANEL_PAD_Y)

        title = tk.Label(header, text=TITLE_TEXT, bg=BG_PRIMARY, fg=FG_ACCENT, font=FONT_TITLE)
        title.pack(anchor="w")

        self.subtitle_label = tk.Label(
            header,
            text=HEADER_TEXT,
            bg=BG_PRIMARY,
            fg=FG_TIMER,
            font=FONT_MONO_BOLD,
            anchor="w",
        )
        self.subtitle_label.pack(anchor="w")

        self.description_label = tk.Label(
            header,
            text=BODY_TEXT,
            bg=BG_PRIMARY,
            fg=FG_DIM,
            font=FONT_MONO,
            anchor="w",
            justify="left",
        )
        self.description_label.pack(anchor="w", pady=(0, PANEL_PAD_Y))

        clocks = tk.Frame(self.root, bg=BG_PRIMARY)
        clocks.pack(fill="x", padx=PANEL_PAD_X, pady=(0, PANEL_PAD_Y))

        deadline_title = tk.Label(
            clocks,
            text=DEADLINE_LABEL_TEXT,
            bg=BG_PRIMARY,
            fg=FG_DIM,
            font=FONT_MONO_BOLD,
        )
        deadline_title.pack(anchor="w")

        self.deadline_label = tk.Label(
            clocks,
            text=self.current_deadline_display(),
            bg=BG_PRIMARY,
            fg=FG_ACCENT,
            font=FONT_DEADLINE,
        )
        self.deadline_label.pack(anchor="w")

        actions = tk.Frame(clocks, bg=BG_PRIMARY)
        actions.pack(anchor="w", pady=(PANEL_PAD_Y, 0))

        reset_btn = tk.Button(
            actions,
            text=RESET_TEXT,
            command=self.reset_round,
            bg=BG_DARK,
            fg=FG_ACCENT,
            relief="flat",
            font=FONT_MONO,
        )
        reset_btn.pack(side="left")

        end_btn = tk.Button(
            actions,
            text=END_TIMER_TEXT,
            command=self.end_round,
            bg=BG_DARK,
            fg=FG_ACCENT,
            relief="flat",
            font=FONT_MONO,
        )
        end_btn.pack(side="left", padx=PANEL_PAD_X)

        self.banner_label = tk.Label(
            self.root,
            text=STATUS_PENDING_TEXT,
            bg=BG_DARK,
            fg=FG_ACCENT,
            font=FONT_MONO_BOLD,
            anchor="w",
        )
        self.banner_label.pack(fill="x", padx=PANEL_PAD_X, pady=(0, PANEL_PAD_Y))

        self.cards_container = tk.Frame(self.root, bg=BG_PRIMARY)
        self.cards_container.pack(fill="both", expand=True, padx=PANEL_PAD_X, pady=(0, PANEL_PAD_Y))
        self.render_cards()

    def render_cards(self) -> None:
        if self.cards_container is None:
            return
        for child in self.cards_container.winfo_children():
            child.destroy()

        self.cards = []
        for index, problem_id in enumerate(self.active_problem_ids, start=1):
            card = build_problem_card(
                parent=self.cards_container,
                num=index,
                pid=problem_id,
                title=PROBLEM_TITLES[problem_id],
                problem_id=problem_id,
                on_select=self.select_file,
                on_submit=self.submit_problem,
                on_open=self.open_problem,
            )
            if problem_id in self.solved_problem_ids:
                card.status_label.configure(text=STATUS_SOLVED_TEXT, fg=FG_SOLVED)
                card.submit_btn.configure(state="disabled")
            elif not self.state.round_active:
                card.submit_btn.configure(state="disabled")
            self.enable_drag_drop(card)
            self.cards.append(card)

    def ensure_sandbox_seeded(self) -> None:
        SANDBOX_PATH.mkdir(parents=True, exist_ok=True)
        if any(SANDBOX_PATH.iterdir()):
            return
        self.restore_sandbox_from_backup()

    def restore_sandbox_from_backup(self) -> bool:
        if not SANDBOX_BACKUP_PATH.exists() or not any(SANDBOX_BACKUP_PATH.iterdir()):
            self.set_banner(STATUS_NO_BACKUP_TEXT, FG_ERROR)
            return False

        SANDBOX_PATH.mkdir(parents=True, exist_ok=True)
        for child in SANDBOX_PATH.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

        for source in SANDBOX_BACKUP_PATH.rglob("*"):
            target = SANDBOX_PATH / source.relative_to(SANDBOX_BACKUP_PATH)
            if source.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

        self.set_banner(STATUS_SANDBOX_RESTORED_TEXT, FG_ACCENT)
        return True

    def encrypt_sandbox(self) -> None:
        if not self.state.encrypted:
            self.ensure_sandbox_seeded()
            encrypted_count = encrypt_all(SANDBOX_PATH)
            self.state.encrypted = True
            save_state(self.state)
            self.set_banner(f"{STATUS_ENCRYPTED_TEXT} ({encrypted_count} files)", FG_ACCENT)

    def decrypt_sandbox(self) -> None:
        if self.state.encrypted:
            decrypt_count = decrypt_all(SANDBOX_PATH)
            self.state.encrypted = False
            self.persist_on_close = False
            clear_state()
            self.set_success_header()
            self.set_banner(f"{STATUS_DECRYPTED_TEXT} ({decrypt_count} files)", FG_SOLVED)

    def refresh_timers(self) -> None:
        if self.deadline_label is not None:
            self.deadline_label.configure(text=self.current_deadline_display())
        self.root.after(TIMER_TICK_MS, self.refresh_timers)

    def current_deadline_display(self) -> str:
        effective_deadline_seconds = max(0, DEADLINE_SECONDS - (self.state.penalties * PENALTY_SECONDS))
        return self.countdown.deadline_display(effective_deadline_seconds)

    def get_card(self, problem_id: str) -> ProblemCard:
        for card in self.cards:
            if card.problem_id == problem_id:
                return card
        raise KeyError(problem_id)

    def enable_drag_drop(self, card: ProblemCard) -> None:
        if DND_FILES is None:
            return
        card.drop_label.drop_target_register(DND_FILES)
        card.drop_label.dnd_bind(
            "<<Drop>>",
            lambda event, pid=card.problem_id: self.on_file_drop(pid, event.data),
        )

    def on_file_drop(self, problem_id: str, raw_data: str) -> None:
        dropped_files = self.root.tk.splitlist(raw_data)
        if not dropped_files:
            return
        dropped_path = dropped_files[0]
        self.attach_file(problem_id, dropped_path)

    def attach_file(self, problem_id: str, selected: str) -> None:
        card = self.get_card(problem_id)
        path = Path(selected)
        if path.suffix.lower() not in {".py", ".cpp"} or not path.is_file():
            self.set_banner(STATUS_INVALID_DROP_TEXT, FG_ERROR)
            card.status_label.configure(text=STATUS_ERROR_TEXT, fg=FG_ERROR)
            return
        card.file_path = str(path)
        card.drop_label.configure(text=path.name)
        card.status_label.configure(text=STATUS_PENDING_TEXT, fg=FG_ACCENT)
        self.set_banner(STATUS_DROPPED_TEXT, FG_ACCENT)

    def select_file(self, problem_id: str) -> None:
        selected = filedialog.askopenfilename(
            title=f"Select solution for problem {problem_id.upper()}",
            filetypes=[("Supported", "*.py *.cpp"), ("Python", "*.py"), ("C++", "*.cpp")],
        )
        if not selected:
            return
        self.attach_file(problem_id, selected)

    def open_problem(self, problem_id: str) -> None:
        viewer = ProblemViewer(self.root, problem_id, PROBLEMS_PATH)
        self.viewer_by_problem[problem_id] = viewer

    def submit_problem(self, problem_id: str) -> None:
        if not self.state.round_active:
            self.set_banner(STATUS_ROUND_ENDED_TEXT, FG_ERROR)
            return

        card = self.get_card(problem_id)
        if not card.file_path:
            self.set_banner(STATUS_NO_FILE_TEXT, FG_ERROR)
            card.status_label.configure(text=STATUS_ERROR_TEXT, fg=FG_ERROR)
            return

        result = judge_submission(card.file_path, problem_id)
        if isinstance(result, dict):
            self.state.penalties += 1
            save_state(self.state)
            card.status_label.configure(text=STATUS_COMPILE_ERROR_TEXT, fg=FG_ERROR)
            self.set_banner(result.get("detail") or STATUS_COMPILE_ERROR_TEXT, FG_ERROR)
            return

        accepted = all(case.get("status") == "AC" for case in result)
        if accepted:
            self.mark_solved(problem_id, card)
            return

        self.state.penalties += 1
        save_state(self.state)
        status = result[0].get("status")
        if status == "TLE":
            card.status_label.configure(text=STATUS_TLE_TEXT, fg=FG_ERROR)
            self.set_banner(STATUS_TLE_TEXT, FG_ERROR)
        elif status == "RTE":
            card.status_label.configure(text=STATUS_RUNTIME_ERROR_TEXT, fg=FG_ERROR)
            self.set_banner(result[0].get("stderr") or STATUS_RUNTIME_ERROR_TEXT, FG_ERROR)
        elif status == "SEGFAULT":
            card.status_label.configure(text=STATUS_SEGFAULT_TEXT, fg=FG_ERROR)
            self.set_banner(result[0].get("stderr") or STATUS_SEGFAULT_TEXT, FG_ERROR)
        else:
            card.status_label.configure(text=STATUS_WRONG_TEXT, fg=FG_ERROR)
            self.set_banner(STATUS_WRONG_TEXT, FG_ERROR)

    def mark_solved(self, problem_id: str, card: ProblemCard) -> None:
        from ransomware.state import sign_solve, verify_solve
        token = sign_solve(problem_id)
        self.state.solve_tokens[problem_id] = token
        self.solved_problem_ids.add(problem_id)
        self.state.solved_problem_ids = sorted(self.solved_problem_ids)
        save_state(self.state)
        card.status_label.configure(text=STATUS_SOLVED_TEXT, fg=FG_SOLVED)
        card.submit_btn.configure(state="disabled")
        self.set_banner(f"Problem {problem_id.upper()} solved.", FG_SOLVED)

        if len(self.solved_problem_ids) >= PROBLEM_COUNT_TO_DECRYPT:
            self.decrypt_sandbox()

    def reset_round(self) -> None:
        restored = self.restore_sandbox_from_backup()
        self.persist_on_close = True
        self.state = RansomwareState(
            started_at=time.time(),
            active_problem_ids=random.sample(PROBLEM_IDS, k=ACTIVE_PROBLEM_COUNT),
            solved_problem_ids=[],
            penalties=0,
            encrypted=False,
            round_active=True,
        )
        self.countdown = Countdown(DEADLINE_SECONDS, started_at=self.state.started_at)
        self.solved_problem_ids = set()
        self.active_problem_ids = list(self.state.active_problem_ids)
        save_state(self.state)
        self.render_cards()
        self.encrypt_sandbox()
        if self.deadline_label is not None:
            self.deadline_label.configure(text=self.current_deadline_display())
        if restored:
            self.set_banner(STATUS_RESET_TEXT, FG_ACCENT)

    def end_round(self) -> None:
        self.persist_on_close = True
        self.state.round_active = False
        self.state.encrypted = False
        save_state(self.state)
        self.restore_sandbox_from_backup()
        self.render_cards()
        self.set_banner(STATUS_ROUND_ENDED_TEXT, FG_ERROR)

    def set_banner(self, text: str, color: str) -> None:
        if self.banner_label is not None:
            self.banner_label.configure(text=text, fg=color)

    def set_success_header(self) -> None:
        if self.subtitle_label is not None:
            self.subtitle_label.configure(text=SUCCESS_HEADER_TEXT, fg=FG_SOLVED)
        if self.description_label is not None:
            self.description_label.configure(text=SUCCESS_BODY_TEXT)

    def on_close(self) -> None:
        if self.persist_on_close:
            self.state.solved_problem_ids = sorted(self.solved_problem_ids)
            save_state(self.state)
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()
