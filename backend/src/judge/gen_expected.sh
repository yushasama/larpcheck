#!/usr/bin/env bash
# gen_expected.sh
# Compiles each solution and runs it against the .in file, writing stdout to .out.
#
# Usage:
#   ./gen_expected.sh              # all problems
#   ./gen_expected.sh a b e        # specific problems
#
# Override dirs via env vars:
#   SOLUTIONS_DIR=../../../solution_code BANK_DIR=../problem_bank ./gen_expected.sh

set -euo pipefail

SOLUTIONS_DIR="${SOLUTIONS_DIR:-../../../solution_code/optimal}"
BANK_DIR="${BANK_DIR:-../problem_bank/testcases}"
BIN_DIR="${BIN_DIR:-/tmp/judge_bins}"

mkdir -p "$BIN_DIR"

ALL_PROBLEMS=("a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l")
PROBLEMS=("${@:-${ALL_PROBLEMS[@]}}")

ok=0
fail=0

for pid in "${PROBLEMS[@]}"; do
    src="$SOLUTIONS_DIR/$pid.cpp"
    bin="$BIN_DIR/$pid"
    inp="$BANK_DIR/$pid.in"
    out="$BANK_DIR/$pid.out"

    if [ ! -f "$src" ]; then
        echo "  [$pid] SKIP - no source at $src"
        continue
    fi
    if [ ! -f "$inp" ]; then
        echo "  [$pid] SKIP - no input at $inp (run build_bank.py first)"
        continue
    fi

    if ! g++ -O2 -std=c++17 -o "$bin" "$src" 2>/tmp/_cerr_$pid; then
        echo "  [$pid] COMPILE ERROR"
        cat /tmp/_cerr_$pid
        ((fail++)) || true
        continue
    fi

    if ! "$bin" < "$inp" > "$out" 2>/tmp/_rerr_$pid; then
        echo "  [$pid] RUNTIME ERROR"
        cat /tmp/_rerr_$pid
        ((fail++)) || true
        continue
    fi

    echo "  [$pid] OK - $(wc -l < "$out") output lines -> $out"
    ((ok++)) || true
done

echo ""
echo "Done. $ok succeeded, $fail failed."

echo "Encrypting .out files..."
python3 -c "
import sys, base64, hashlib
from pathlib import Path
from cryptography.fernet import Fernet
sys.path.insert(0, str(Path('$BANK_DIR').parent.parent / 'ransomware'))
from config import FERNET_SECRET, FERNET_SALT

key = hashlib.scrypt(FERNET_SECRET, salt=FERNET_SALT, n=2**14, r=8, p=1, dklen=32)
f = Fernet(base64.urlsafe_b64encode(key))

for p in Path('$BANK_DIR').glob('*.out'):
    p.with_suffix('.out.enc').write_bytes(f.encrypt(p.read_bytes()))
    p.unlink()
    print(f'  encrypted {p.stem}.out.enc')
"
echo "Encryption done."
