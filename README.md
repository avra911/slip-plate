# SLIP-P: Shamir DEK Plates

SLIP-P is a Python implementation for visualizing Shamir-split DEKs on plates, similar to OneKey KeyTag. Supports 128, 192, 256-bit DEKs and dynamic checksum.

## Installation

```bash
git clone https://github.com/avra911/slip-plate.git
cd slip-plate
pip install -r requirements.txt
```

## Usage

```python
from slip_plate.main import main

main()
```

### Example usage

Run the example script with a specific DEK size:

```bash
python -m examples.example_run --dek 256
```

This will generate a 256-bit DEK, split it into Shamir shares, print the plates and then recover the DEK to decrypt the message.

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
