from ransomware.runtime.paths import (
    APP_ROOT,
    BACKEND_PATH,
    BUNDLE_ROOT,
    PACKAGE_PATH,
    PROBLEMS_PATH,
    REPO_ROOT,
    RESOURCES_PATH,
    SANDBOX_BACKUP_PATH,
    SANDBOX_PATH,
    SRC_PATH,
    STATE_PATH,
    TESTCASES_PATH,
)

FERNET_SECRET = b"larpcheck-2026"
FERNET_SALT = b"testcase-salt"

AES_KEY = bytes.fromhex("7dbe78781e7cd0bc9ec34f938e0576a6582431d179dbc794272fe873a2d6ab6a")
AES_NONCE_SIZE = 12
AES_TAG_SIZE = 16
ENCRYPTED_FILE_MAGIC = b"LARPCHK1"
DEADLINE_SECONDS = 72 * 3600
PENALTY_SECONDS = 8 * 3600
WINDOW_SIZE = "1000x800"
VIEWER_WINDOW_SIZE = "800x600"

TIMER_TICK_MS = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
ZERO_TIME = "00:00"
ZERO_DEADLINE = "00:00:00"

TITLE_TEXT = "LarpCheck"
HEADER_TEXT = "YOUR FILES HAVE BEEN ENCRYPTED"
BODY_TEXT = (
    "Someone wasn't paying attention in their cybersecurity class and downloaded a virus from weird sites :((!\n"
    "It's okay though! As long as you've been grinding your DSA interview prep, it's no issue.\n"
    "Just solve the problems given below to recover your (sandboxed) files.\n"
    "Otherwise, your encrypted files will get deleted (not literally because demo reasons)\n"
    "and you'll get exposed as larping as a programmer xDD"
)
SUCCESS_HEADER_TEXT = "YOU PASSED THE LARP CHECK!"
SUCCESS_BODY_TEXT = (
    "Congrats, you proved your skills as a CS major thus your files are safe and sound!\n"
)
DEADLINE_LABEL_TEXT = "Global Deadline"
SELECT_FILE_TEXT = "Select File"
DROP_FILE_TEXT = "Select or drop a .py / .cpp file"
OPEN_PROBLEM_TEXT = "Open Problem"
SUBMIT_TEXT = "Submit"
RESET_TEXT = "Reset"
END_TIMER_TEXT = "End Timer"
STATUS_PENDING_TEXT = "Pending"
STATUS_SOLVED_TEXT = "Accepted Code"
STATUS_WRONG_TEXT = "Wrong Answer"
STATUS_TLE_TEXT = "Time Limit Exceeded"
STATUS_RUNTIME_ERROR_TEXT = "Runtime Error"
STATUS_SEGFAULT_TEXT = "Segmentation Fault"
STATUS_COMPILE_ERROR_TEXT = "Compile Error"
STATUS_ERROR_TEXT = "Error"
STATUS_NO_FILE_TEXT = "Select a file first."
STATUS_DROPPED_TEXT = "File attached."
STATUS_INVALID_DROP_TEXT = "Drop a valid .py or .cpp file."
STATUS_DECRYPTED_TEXT = "Sandbox restored."
STATUS_ENCRYPTED_TEXT = "Sandbox encrypted."
STATUS_RESET_TEXT = "Round reset and sandbox encrypted."
STATUS_ROUND_ENDED_TEXT = "Round ended. Submissions disabled."
STATUS_SANDBOX_RESTORED_TEXT = "Sandbox restored from backup."
STATUS_NO_BACKUP_TEXT = "sandbox_backup is missing or empty."
VIEWER_MISSING_TEXT = "<h3>Problem file not found.</h3>"

PANEL_PAD_X = 14
PANEL_PAD_Y = 10
CARD_BUTTON_WIDTH = 12
TITLE_WRAP_LENGTH = 420
BODY_WRAP_LENGTH = 620
DROP_WRAP_LENGTH = 300
ACTIVE_PROBLEM_COUNT = 3
PROBLEM_COUNT_TO_DECRYPT = ACTIVE_PROBLEM_COUNT

PROBLEM_IDS = tuple("abcdefghijkl")
PROBLEM_TITLES = {
    "a": "Special Week's Training Log",
    "b": "Tung Tung Tung Sahur vs Larp Larp Larp Sahur",
    "c": "Nokotan's Antler Count",
    "d": "Super Creek's Training Ground",
    "e": "Netflix Releases Steel Ball Run (Fans Are Not Okay)",
    "f": "The Larp Circle",
    "g": "Kazuma's Marketing Empire (Don't Let Them Repo The Urus)",
    "h": "Subaru's Piezoelectric Staircase",
    "i": "Ayanokoji's Exposure Protocol",
    "j": "Kazuma's Eris Heist",
    "k": "The M3 Down Payment",
    "l": "Kazuma's Course Launch Party (The Urus Is Already Leased)",
}
