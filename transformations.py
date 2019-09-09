import mido
import time

def calc_octave_down(msg, time_between_notes):
    """
    Returns a note that is an octave down from the note that is input.

    msg: mido.Message
    """
    new_note = 0
    if msg.note < 33:
        new_note = msg.note
    else:
        new_note = msg.note - 12
    return mido.Message('note_on', note=new_note, velocity=msg.velocity, time=time.time() + time_between_notes)

def calc_inverse(msg):
    """
    Returns a note that is reflected across the axis of symmetry on the piano.

    note: mido.Mesasge

    Return mido.Message
    """
    new_note = 0
    if msg.note > 65:
        diff = msg.note - 65
        new_note = 64 - diff
    elif msg.note < 64:
        diff = 64 - msg.note
        new_note = 65 + diff
    elif msg.note == 64:
        new_note = 65
    elif msg.note == 65:
        new_note = 64
    return mido.Message('note_on', note=new_note, velocity=msg.velocity)
