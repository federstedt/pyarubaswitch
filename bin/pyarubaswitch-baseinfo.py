#!/usr/bin/python3

import pyarubaswitch


def main():
    print("Lets go!")
    # via yaml
    run_1 = pyarubaswitch.BaseInfoGetter(verbose=True, SSL=True)
    # with args

    # with input

    run_1.get_info()


if __name__ == "__main__":
    main()