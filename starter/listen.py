"""House Voice — microphone helpers: wake detection, recording, transcribing.

Each piece degrades gracefully: if openWakeWord isn't installed, push-to-talk
(Enter key) is used; if no STT engine is installed, it asks you to type — so
the script never hard-fails on an evening, it just asks for a bigger role.
(All heavy imports are done inside functions so --text mode needs nothing.)
"""

import os
import time

import config


def list_input_devices():
    """Run with --devices to see every microphone the OS offers."""
    import sounddevice as sd
    print("Input (microphone) devices:")
    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0:
            print(f"  [{i}] {dev['name']!r}  ({dev['max_input_channels']} ch, "
                  f"{int(dev['default_samplerate'])} Hz)")
    print("Set INPUT_DEVICE_INDEX in config.py to a number, or leave None "
          "for the OS default. See docs/troubleshooting.md rows 6-7.")


def get_stt():
    """Returns a transcriber object, or None (type-fallback mode)."""
    if config.STT_ENGINE == "faster-whisper":
        try:
            from faster_whisper import WhisperModel
            return WhisperModel(config.STT_MODEL, device="cpu", compute_type="int8")
        except ImportError:
            import sys
            sys.exit("Missing faster-whisper. Run: pip install faster-whisper "
                     "(or set STT_ENGINE='vosk' in config.py — see chapter 4)")
    if config.STT_ENGINE == "vosk":
        try:
            from vosk import Model
            return Model("vosk-model-small-en-us-0.15")   # download once, keep local
        except ImportError:
            import sys
            sys.exit("Missing vosk. Run: pip install vosk "
                     "(or set STT_ENGINE='faster-whisper' in config.py)")
    return None


def _input_stream(sd, sample_rate=16000):
    kwargs = {"samplerate": sample_rate, "channels": 1, "dtype": "int16",
              "blocksize": 1280}
    if config.INPUT_DEVICE_INDEX is not None:
        kwargs["device"] = config.INPUT_DEVICE_INDEX
    return sd.InputStream(**kwargs)


def detect_wake_word():
    """True once the wake word is heard; Enter-key push-to-talk otherwise."""
    try:
        import numpy as np
        from openwakeword.model import Model as OWW
        import sounddevice as sd
        oww = OWW()
        print(f"Wake engine: openWakeWord, listening for '{config.WAKE_WORD}'.")
        with _input_stream(sd) as stream:
            while True:
                frames, _overflow = stream.read(1280)
                for chunk in frames:
                    scores = oww.predict(np.frombuffer(chunk.tobytes(), dtype=np.int16))
                    top = max(scores, key=scores.get)
                    if scores[top] >= 0.5:
                        print("Wake!")
                        return True
    except ImportError:
        print(f"openWakeWord not installed — push-to-talk mode instead "
              f"(wake word '{config.WAKE_WORD}' is decorative tonight). "
              f"See docs/02-wake-words.md.")
        input("Press Enter, then speak: ")
        return True


def record_sentence(sd, stt, max_seconds=8, sample_rate=16000):
    """Record until ~1.2 s of silence, max 8 s. Returns a wav path or None."""
    import numpy as np
    try:
        import soundfile as sf
    except ImportError:
        sf = None
    frames, since_voice = [], 0
    thresh = 300                                   # int16 RMS floor for "someone spoke"
    with _input_stream(sd, sample_rate) as stream:
        print("Listening for your sentence...")
        started = time.time()
        while time.time() - started < max_seconds:
            data, _overflow = stream.read(int(sample_rate * 0.1))
            arr = np.frombuffer(data.tobytes(), dtype=np.int16)
            frames.append(data)
            if np.sqrt(np.mean(arr.astype("float32") ** 2)) > thresh:
                since_voice = 0
            else:
                since_voice += 1
                if since_voice >= 12 and len(frames) > 12:   # ~1.2 s of quiet
                    break
    if sf is None:
        return None
    path = os.path.join(config.DATA_DIR, "last_command.wav")
    sf.write(path, np.concatenate(frames).astype(np.int16), sample_rate)
    return path


def transcribe(stt, wav_path):
    """The text for what you said — or, with no engine installed, typed input."""
    if stt is None or not wav_path:
        return input("(no audio engine — type your sentence instead): ").strip()
    segments, _info = stt.transcribe(wav_path, language="en")
    return " ".join(s.text for s in segments).strip()
