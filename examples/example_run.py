import argparse

from slip_plate.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dek-size", type=int, choices=[128, 192, 256], default=256)
    parser.add_argument("--parts", type=int, default=3)
    parser.add_argument("--threshold", type=int, default=2)
    args = parser.parse_args()
    main(args.dek_size, args.parts, args.threshold)
