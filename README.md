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
cd backend/src
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

From the repo root:

```bash
cd compile_app
```

Mac/Linux:
```bash
./compile.sh
```

Windows:
```bat
build.bat
```

Windows PowerShell:
```powershell
.\build.bat
```

The build scripts run PyInstaller in the `backend/src` uv project, so project dependencies like `tkinterweb` and `tkinterdnd2` are included in the packaged app. Output lands in `compile_app/dist/LarpCheck/` on both Mac/Linux and Windows, with the launcher at `compile_app/dist/LarpCheck/LarpCheck` or `compile_app/dist/LarpCheck/LarpCheck.exe`.

The packaged app bundles:
- problem HTML from `backend/src/ransomware/resources/problems`
- encrypted testcase files from `backend/src/problem_bank/testcases`
- a default `sandbox_backup/` seed set

The packaged app does not bundle plaintext expected outputs or reference solution source files.

When you launch the packaged app, writable runtime files are created next to the launcher:
- `sandbox/`
- `.larpcheck_state.json`

---

## Project Structure

```text
backend/src/
|-- ransomware/               <- main app package
|   |-- __main__.py           <- entry point
|   |-- config.py             <- all constants and paths
|   |-- crypto.py             <- AES-GCM sandbox encryption + Fernet for testcases
|   |-- state.py              <- persistent round state + HMAC solve tokens
|   |-- countdown.py          <- deadline timer
|   |-- security.py           <- debugger detection
|   |-- ui/
|   |   |-- app.py            <- main UI controller
|   |   |-- problem_card.py   <- per-problem UI card
|   |   |-- problem_viewer.py <- embedded HTML problem viewer
|   |   `-- styles.py         <- color and font constants
|   `-- resources/problems/   <- bundled HTML problem statements
|-- judge/
|   |-- judge.py              <- local C++/Python judge
|   |-- gen_testcases.py      <- generates .in testcase files
|   `-- get_expected.sh       <- generates and encrypts .out files
`-- problem_bank/
    |-- *.json                <- problem definitions
    `-- testcases/            <- .in and .out.enc files
```

---

## How It Works

**On startup**, the app checks for an attached debugger. If one is detected, it exits immediately with no warning. If clean, it loads persistent round state, seeds `sandbox/` from `sandbox_backup/` if empty, assigns 3 random problems from a pool of 12, and encrypts the sandbox. In a packaged build, bundled read-only assets are loaded from the app bundle while writable runtime files live beside the launcher.

**To unlock**, the student submits `.py` or `.cpp` solutions for each assigned problem. The judge compiles and runs them locally against encrypted testcases. Wrong answers add an 8-hour penalty to the global deadline. Solving all 3 problems triggers decryption.

**Anti-tamper**, each correct solve generates an HMAC-SHA256 token tied to that problem ID. Decryption requires all tokens to verify. Patching memory or editing the state file does nothing without valid tokens.

**Testcase protection**, expected outputs are encrypted with Fernet and only decrypted in memory during judging. No plaintext answers exist on disk after the build step.

**Problem viewer**, problem statements render inside the app via `tkinterweb`. No external browser is ever opened.

---

## Sandbox

The `sandbox/` folder is what gets encrypted. It is seeded automatically from `sandbox_backup/` on first run or after a reset.

In source mode, `sandbox/` and `sandbox_backup/` live at the repo root.

In the packaged app, `sandbox/` is created next to `LarpCheck.exe`. If a sibling `sandbox_backup/` folder exists there, the app uses it. Otherwise it falls back to the bundled default backup.

To customize the packaged demo files, drop your own `sandbox_backup/` next to the EXE before launching.

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

## References

This project uses the following Python and cryptography APIs:

- AES-GCM via `cryptography.hazmat.primitives.ciphers.aead.AESGCM` for sandbox file encryption. The `cryptography` docs describe AES-GCM as an AEAD construction and warn that nonce reuse with the same key compromises security. They also note that the nonce does not need to be secret and may be included with the ciphertext. Docs: https://cryptography.io/en/latest/hazmat/primitives/aead/

- Fernet via `cryptography.fernet.Fernet` for encrypted expected outputs. The `cryptography` docs describe Fernet as symmetric authenticated cryptography where encrypted messages cannot be read or modified without the key. Docs: https://cryptography.io/en/stable/fernet/

- `hashlib.scrypt` for deriving the Fernet key from a project secret and salt. Python's `hashlib` documentation covers `scrypt` as a password-based key derivation function. Docs: https://docs.python.org/3/library/hashlib.html#hashlib.scrypt

- `hmac.new` and `hmac.compare_digest` for solve-token signing and verification. Python's `hmac` documentation describes HMAC as keyed hashing for message authentication and recommends `compare_digest` for verification comparisons. Docs: https://docs.python.org/3/library/hmac.html

- `subprocess.run` for compiling and executing submitted Python/C++ code during judging. Python's `subprocess` documentation covers process execution, timeout handling, and security considerations. Docs: https://docs.python.org/3/library/subprocess.html

- `tempfile.TemporaryDirectory` for creating temporary workspaces during judging. Python's `tempfile` documentation describes temporary files/directories and automatic cleanup through context-manager usage. Docs: https://docs.python.org/3/library/tempfile.html

These references document the libraries and primitives used in the implementation; they are not claims that the current local-only design is secure against reverse engineering.
