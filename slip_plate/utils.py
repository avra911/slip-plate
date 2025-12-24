import hashlib

def bytes_to_bits(b: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in b)

def bits_to_bytes(bstr: str) -> bytes:
    return bytes(int(bstr[i:i+8], 2) for i in range(0, len(bstr), 8))

def determine_checksum_bits(bits_len: int) -> int:
    """Decide dynamic checksum bits based on share size"""
    if bits_len <= 144:    # 128-bit DEK
        return 8
    elif bits_len <= 204:  # 192-bit DEK
        return 16
    else:                  # 256-bit DEK
        return 24

def determine_plate_checksum_bits(bits_len: int) -> int:
    """Decide dynamic checksum bits based on plate share size"""
    if bits_len <= 144:    # 128-bit DEK
        return 8
    elif bits_len <= 216:  # 192-bit DEK
        return 16
    else:                  # 256-bit DEK
        return 24

def add_checksum(bits: str, bits_per_row=12) -> str:
    """Add checksum on the last rows dynamically"""
    checksum_bits_len = determine_checksum_bits(len(bits))
    h = hashlib.sha256(bits.encode()).hexdigest()
    checksum_bits = bin(int(h, 16))[2:].zfill(256)[:checksum_bits_len]
    return bits + checksum_bits

def bits_to_plate(bits: str, bits_per_row=12, group=4) -> str:
    """Return OneKey-style plate with vertical header and checksum bits highlighted."""
    
    # Determine number of checksum bits dynamically
    checksum_bits = determine_plate_checksum_bits(len(bits))
    total_bits = len(bits)

    total_rows = (total_bits + bits_per_row - 1) // bits_per_row

    plate_lines = []

    # Build vertical header
    columns = [2**i for i in reversed(range(bits_per_row))]
    col_strs = [str(c).rjust(4) for c in columns]
    max_digit_len = max(len(c) for c in col_strs)
    
    for row in range(max_digit_len):
        line_parts = []
        for i, c in enumerate(col_strs):
            char = c[row] if row < len(c) else ' '
            line_parts.append(f" {char}")
            if (i+1) % group == 0 and (i+1) != bits_per_row:
                line_parts.append(" │")
        plate_lines.append("    " + "".join(line_parts))

    # Separator under header
    plate_lines.append("    " + "─" * (bits_per_row*2 + 5))

    # ANSI colors
    COLOR_DATA = "\033[97m"      # white
    COLOR_CHECKSUM = "\033[93m"  # yellow
    COLOR_RESET = "\033[0m"

    # Rows
    bit_index = 0
    for r in range(total_rows):
        row_bits = bits[r*bits_per_row:(r+1)*bits_per_row].ljust(bits_per_row, '0')
        row_parts = []
        for b in row_bits:
            color = COLOR_CHECKSUM if bit_index >= total_bits - checksum_bits else COLOR_DATA
            row_parts.append(f"{color}{'●' if b=='1' else '○'}{COLOR_RESET}")
            bit_index += 1
        # group separators
        for g in range(group-1):
            row_parts.insert((g+1)*group + g, "│")
        plate_lines.append(f"{r+1:2} | " + " ".join(row_parts))

    # Final line
    plate_lines.append("    " + "─" * (bits_per_row*2 + 5))
    return "\n".join(plate_lines)
