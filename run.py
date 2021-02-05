from workflows.get_base_info import BaseInfoGetter


def main():
    print("Lets go!")
    # via yaml
    run_1 = BaseInfoGetter("vars.yaml", verbose=True, SSL=True)
    # with args

    # with input

    run_1.get_info()
    # print(run_1.switches)


if __name__ == "__main__":
    main()
