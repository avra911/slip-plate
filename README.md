# SLIP-P: Shamir DEK Plates

SLIP-P is a small Python demo that shows how to split DEKs (128/192/256-bit) with
Shamir secret sharing and render OneKey-style plates with a small checksum.

This repository was refactored into modular components (CLI, checksum, plate
renderer, Shamir wrappers, and crypto helpers) and includes unit tests.

## Installation

Quick (no editable install):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
PYTHONPATH=. pytest -q
```

Recommended (editable install so package imports work automatically):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
# then (optional) install editable if you added pyproject/setup.cfg
pip install -e .
pytest -q
```

If you don't want to install, setting `PYTHONPATH=.` before `pytest` or running
the CLI via `python -m slip_plate.cli` will work.

## Usage

This will generate a 256-bit DEK, split it into Shamir shares, print the plates and then recover the DEK to decrypt the message.

Run the CLI/demo:

```bash
python -m slip_plate.cli --dek-size 256 --parts 3 --threshold 2
```

Run the example runner:

```bash
python -m examples.example_run --dek-size 256 --parts 3 --threshold 2
```

### Example OneKey-style Plate

Below is a randomized example output for a KEK share plate (128-bit DEK, 2-of-3 Shamir):

```bash
=== Shares OneKey-style ===

=== KEK Share 1 ===
     2 1     │         │        
     0 0 5 2 │ 1       │        
     4 2 1 5 │ 2 6 3 1 │        
     8 4 2 6 │ 8 4 2 6 │ 8 4 2 1
    ─────────────────────────────
 1 | ○ ● ● ● │ ● ○ ○ ● │ ● ● ○ ○ │
 2 | ○ ○ ● ○ │ ○ ○ ○ ○ │ ○ ○ ● ○ │
 . | . . . . | . . . . | . . . . |
 . | . . . . | . . . . | . . . . |
 . | . . . . | . . . . | . . . . |
11 | ○ ○ ○ ● │ ● ● ● ○ │ ○ ○ ● ○ │
12 | ● ● ○ ○ │ ● ● ○ ● │ ● ○ ○ ○ │
    ─────────────────────────────
```

Dots (…) represent truncated rows for brevity.

### Security Model

- Plates are generated once and stored offline
- DEKs are reconstructed from a quorum of shares during encryption or decryption
- Nonces are unique per encryption and embedded in the ciphertext
- No DEK is stored digitally outside memory during use


### Tests

Run all tests:

```bash
pytest -q
```

Run a single test file:

```bash
pytest tests/test_shamir.py -q
```

## Notes and caveats

- Tests include a basic end-to-end flow that encrypts data, splits the DEK, recovers it and decrypts to verify correctness.
- The plate renderer uses ANSI symbols/colors for terminal output.
- **This is a demo / research tool - treat outputs as examples and review the code and cryptographic choices before using in production.**
- Keep printed plates physically secure; the checksum helps detect transcription errors but is not a replacement for proper key management.

Contributions welcome - open a PR or an issue on the repo if you have improvements or questions.
