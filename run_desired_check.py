from workflows.check_desired_vlans import PortChecker


def main():
    untag = [119]
    tag = [99, 1, 128]
    print(f"Desired untag: {untag}")
    print(f"Desired tagged {tag}")
    port_check = PortChecker(untag, tag, verbose=True, SSL=True)
    port_check.check_switches()


if __name__ == "__main__":
    main()
