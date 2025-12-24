import argparse

from .main import main


def build_parser():
    parser = argparse.ArgumentParser(description="Slip-plate demo CLI")
    parser.add_argument("--dek-size", type=int, choices=[128, 192, 256], default=256)
    parser.add_argument("--parts", type=int, default=3)
    parser.add_argument("--threshold", type=int, default=2)
    return parser


def run():
    parser = build_parser()
    args = parser.parse_args()
    main(args.dek_size, args.parts, args.threshold)


if __name__ == "__main__":
    run()
