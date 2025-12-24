import argparse

from slip_plate.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dek", type=int, choices=[128, 192, 256], default=256)
    args = parser.parse_args()
    main(args.dek)
