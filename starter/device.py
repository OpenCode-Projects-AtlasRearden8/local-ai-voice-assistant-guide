"""House Voice — print every microphone input the OS offers (troubleshooting #7)."""

import listen


if __name__ == "__main__":
    listen.list_input_devices()
