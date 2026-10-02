"""Entry point:  python -m jarvis"""
from jarvis.core.assistant import Assistant


def main() -> None:
    Assistant().greet()


if __name__ == "__main__":
    main()
