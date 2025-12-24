from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pyshamir import split, combine
import os
import random
from .utils import bytes_to_bits, bits_to_bytes, add_checksum, bits_to_plate, determine_checksum_bits

def prepare_share(s_bytes: bytes) -> str:
    bits = bytes_to_bits(s_bytes)
    return add_checksum(bits)

def recover_dek_from_shares(shares_bin) -> bytes:
    recovery_bytes = []
    for idx, s in enumerate(shares_bin, 1):
        checksum_bits_len = determine_checksum_bits(len(s)-determine_checksum_bits(len(s)))
        if len(s) < checksum_bits_len:
            raise ValueError(f"Share {idx} too short for checksum!")

        data_bits = s[:-checksum_bits_len]
        checksum_bits = s[-checksum_bits_len:]

        import hashlib
        h = hashlib.sha256(data_bits.encode()).hexdigest()
        expected_checksum = bin(int(h, 16))[2:].zfill(256)[:checksum_bits_len]

        if checksum_bits != expected_checksum:
            raise ValueError(f"Checksum invalid on Share {idx}!")

        recovery_bytes.append(bits_to_bytes(data_bits))

    return combine(recovery_bytes)

def main(dek_size=256):
    plaintext = b"Secret message encrypted with DEK"
    dek = AESGCM.generate_key(bit_length=dek_size)
    aesgcm_dek = AESGCM(dek)
    nonce = os.urandom(12)
    header = b"ENC1v1AESGCM256"

    ciphertext = aesgcm_dek.encrypt(nonce, plaintext, header)
    blob = header + nonce + ciphertext
    print("Encrypted blob (hex):", blob.hex())

    shares_bytes = split(dek, 3, 2)
    shares_bin = [prepare_share(s) for s in shares_bytes]

    print(f"\n=== Shares OneKey-style ===")
    for idx, sh in enumerate(shares_bin, 1):
        print(f"\n=== KEK Share {idx} ===")
        print(bits_to_plate(sh))

    random.shuffle(shares_bin)
    recovery_bin = shares_bin[:2]
    recovered_dek = recover_dek_from_shares(recovery_bin)

    aesgcm_recovered = AESGCM(recovered_dek)
    parsed_header = blob[:len(header)]
    parsed_nonce = blob[len(header):len(header)+12]
    parsed_ciphertext = blob[len(header)+12:]
    decrypted = aesgcm_recovered.decrypt(parsed_nonce, parsed_ciphertext, parsed_header)

    print("\nDecrypted plaintext:", decrypted)
    print("Recovery and decryption successful:", decrypted == plaintext)
