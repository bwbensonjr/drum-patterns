 # (Save this as play_midi_with_samples.py)
import mido
import pygame

def main():
    # --- Configuration ---
    MIDI_FILE = 'my_rock_beat.mid' # The file we just generated

    # The audio samples we will use
    SAMPLES = {
        "kick": "kick.wav",
        "snare": "snare.wav",
        "hat": "hat.wav",
        "open_hat": "open_hat.wav" # Add more if your MIDI uses them
    }

    # This is the crucial mapping from MIDI note number to our sample key
    # These are standard General MIDI (GM) drum notes
    NOTE_MAP = {
        36: "kick",      # Bass Drum 1
        38: "snare",     # Acoustic Snare
        42: "hat",       # Closed Hi-Hat
        46: "open_hat",  # Open Hi-Hat
        # Add other mappings here as needed
        # 49: "crash",
        # 51: "ride",
    }

    # --- Initialization ---
    print("Initializing audio player...")
    pygame.mixer.init()

    # Load the sound files into pygame Sound objects
    sounds = {name: pygame.mixer.Sound(file) for name, file in SAMPLES.items()}

    # Load the MIDI file
    try:
        mid = mido.MidiFile(MIDI_FILE)
        print(f"Successfully loaded '{MIDI_FILE}'")
    except FileNotFoundError:
        print(f"Error: The MIDI file '{MIDI_FILE}' was not found.")
        print("Please run the 'generate_midi.py' script first.")
        exit()


    # --- The Player Loop ---
    print("\nPlaying MIDI file with samples. Press Ctrl+C to stop.")
    try:
        # mido's play() function is a generator that yields messages in real-time
        # It automatically handles the timing for us!
        for msg in mid.play():
            # We only care about 'note_on' messages with a velocity > 0
            # (A 'note_on' with velocity 0 is often used as a 'note_off')
            if msg.type == 'note_on' and msg.velocity > 0:
                # Look up the note number in our map
                sound_name = NOTE_MAP.get(msg.note)

                # If the note is in our map and we have a sample for it...
                if sound_name and sound_name in sounds:
                    # ...play the sound!
                    print(f"Playing note {msg.note}: {sound_name}")
                    sounds[sound_name].play()
                else:
                    print(f"Note {msg.note} has no mapped sample. Skipping.")

    except KeyboardInterrupt:
        print("\nPlayback stopped by user.")
    finally:
        # Clean up the mixer when we're done
        pygame.mixer.quit()
        print("Player shut down.")

