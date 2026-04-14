# LarpCheck

A ransomware simulation app built for educational purposes as a semester project. When launched, it encrypts files in a local `sandbox/` folder using AES-GCM. To decrypt them, you have to solve 3 randomly assigned DSA programming problems and submit correct solutions.

Everything is self-contained. No internet, no servers, runs entirely locally.

> This project is for educational purposes only. Do not deploy against any system without explicit written consent.

---

## Requirements

- Python 3.11+
- `uv` (package manager)
- `g++` with C++17 support (for judging C++ submissions)

---

## Setup

```bash
# clone the repo
git clone <repo-url>
cd larpcheck

# install dependencies
cd backend/src/ransomware
uv sync
```

---

## Dev Workflow

### 1. Generate testcase inputs

```bash
cd backend/src/judge
python gen_testcases.py
```

### 2. Generate expected outputs and encrypt them

Mac/Linux:
```bash
./get_expected.sh
```

This compiles the reference solutions, runs them against the inputs, encrypts the outputs to `.out.enc`, and deletes the plaintext `.out` files. No plaintext answers are ever stored after this step.

### 3. Run the app

```bash
cd backend/src
uv run python -m ransomware
```

---

## Building the Exe

Mac/Linux:
```bash
./build.sh
```

Windows:
```bat
build.bat
```

Output lands in `dist/LarpCheck` (or `dist/LarpCheck.exe` on Windows). Only `.out.enc` files are bundled, never plaintext answers or source files.

---

## Project Structure

```
backend/src/
├── ransomware/               <- main app package
│   ├── __main__.py           <- entry point
│   ├── config.py             <- all constants and paths
│   ├── crypto.py             <- AES-GCM sandbox encryption + Fernet for testcases
│   ├── state.py              <- persistent round state + HMAC solve tokens
│   ├── countdown.py          <- deadline timer
│   ├── security.py           <- debugger detection
│   ├── ui/
│   │   ├── app.py            <- main UI controller
│   │   ├── problem_card.py   <- per-problem UI card
│   │   ├── problem_viewer.py <- embedded HTML problem viewer
│   │   └── styles.py         <- color and font constants
│   └── resources/problems/   <- bundled HTML problem statements
├── judge/
│   ├── judge.py              <- local C++/Python judge
│   ├── gen_testcases.py      <- generates .in testcase files
│   └── get_expected.sh       <- generates and encrypts .out files
└── problem_bank/
    ├── *.json                <- problem definitions
    └── testcases/            <- .in and .out.enc files
```

---

## How It Works

**On startup**, the app checks for an attached debugger. If one is detected, it exits immediately with no warning. If clean, it loads persistent round state, seeds `sandbox/` from `sandbox_backup/` if empty, assigns 3 random problems from a pool of 12, and encrypts the sandbox.

**To unlock**, the student submits `.py` or `.cpp` solutions for each assigned problem. The judge compiles and runs them locally against encrypted testcases. Wrong answers add an 8-hour penalty to the global deadline. Solving all 3 problems triggers decryption.

**Anti-tamper**, each correct solve generates an HMAC-SHA256 token tied to that problem ID. Decryption requires all tokens to verify. Patching memory or editing the state file does nothing without valid tokens.

**Testcase protection**, expected outputs are encrypted with Fernet and only decrypted in memory during judging. No plaintext answers exist on disk after the build step.

**Problem viewer**, problem statements render inside the app via `tkinterweb`. No external browser is ever opened.

---

## Sandbox

The `sandbox/` folder is what gets encrypted. It is seeded automatically from `sandbox_backup/` on first run or after a reset. Put whatever demo files you want in `sandbox_backup/` before running.

---

## Resetting a Round

Click the `Reset` button in the app. This restores `sandbox/` from backup, picks 3 new random problems, resets the timer and penalties, and starts a fresh encrypted round.

---

## Problems

There are 12 problems in the pool, labeled `a` through `l`:

| ID | Title | Topic |
|----|-------|-------|
| a | Special Week's Training Log | FizzBuzz / Simulation |
| b | Tung Tung Tung Sahur vs Larp Larp Larp Sahur | Binary Search |
| c | Nokotan's Antler Count | Prefix Sums |
| d | Super Creek's Training Ground | Euler Tour + Subtree Queries |
| e | Netflix Releases Steel Ball Run (Fans Are Not Okay) | Interval DP |
| f | The Larp Circle | Graph Construction |
| g | Kazuma's Marketing Empire (Don't Let Them Repo The Urus) | Dijkstra |
| h | Subaru's Piezoelectric Staircase | Euler Tour + BIT |
| i | Ayanokoji's Exposure Protocol | Bitmask DP |
| j | Kazuma's Eris Heist | Rerooting Tree DP |
| k | The M3 Down Payment | Two Sum (Hashmap) |
| l | Kazuma's Course Launch Party (The Urus Is Already Leased) | 3Sum + BFS |

Problem statements are HTML files bundled in `resources/problems/`. Reference solutions live in `solution_code/optimal/`.