import time

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Engine v1")
    parser.add_argument("--param_1", type=str, default=None)
    parser.add_argument("--param_2", type=float, default=1)
    parser.add_argument("--param_3", type=bool, default=None)

    args = parser.parse_args()

    print(f"--param_1: {args.param_1}")
    print(f"--param_2: {args.param_2}")
    print(f"--param_3: {args.param_3}")

    if args.param_3 is True:
        time.sleep(args.param_2)

    print(f"RESULT = {args.param_1}")
