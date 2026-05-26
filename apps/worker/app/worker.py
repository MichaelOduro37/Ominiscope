from rq import Connection, Worker

from app.queue import get_connection, get_queue


def main() -> None:
    connection = get_connection()
    queue = get_queue()
    with Connection(connection):
        Worker([queue]).work()


if __name__ == "__main__":
    main()
