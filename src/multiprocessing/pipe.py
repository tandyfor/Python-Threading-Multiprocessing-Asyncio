from multiprocessing import Process, Pipe

class CustomClass:
    pass

def work(connection):
    while True:
        instance = connection.recv()

        if instance:
            print(f"CHLD: {instance}")

        else:
            return
        
def main():
    parent_conn, child_conn = Pipe()

    child = Process(target=work, args=(child_conn, ))

    for item in (
        42,
        "some string",
        {'one': 1},
        CustomClass(),
        None
    ):
        print(f"PRNT: send {item}")
        parent_conn.send(item)

    child.start()
    child.join()

if __name__ == "__main__":
    main()