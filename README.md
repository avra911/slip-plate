# SLIP-P: Shamir DEK Plates

SLIP-P is a Python implementation for visualizing Shamir-split DEKs on plates, similar to OneKey. Supports 128, 192, 256-bit DEKs and dynamic checksum.

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

This will generate a 256-bit DEK, split it into Shamir shares, print the plates, and then recover the DEK to decrypt the message.

