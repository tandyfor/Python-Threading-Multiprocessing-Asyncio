import os

pid_list = []

def main():
    pid_list.append(os.getpid())
    child_pid = os.fork()

    if child_pid == 0:
        pid_list.append(os.getpid())
        print()
        print("CHLD PRC")
        print(f"CHLD pids: {pid_list}")

    else:
        pid_list.append(os.getpid())
        print()
        print("PRNT PRC")
        print(f"PRNT pids: {pid_list}")


if __name__ == "__main__":
    main()