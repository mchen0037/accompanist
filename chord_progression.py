import mido
import time

from transformations import calc_octave_down

"""
Hold pedal to "record" notes to loop.
Let go to play along to the loop.
Double tap to delete the recording.
"""

left = 64
right = 65
notes = {
    21: 'A0',
    22: 'A#0',
    23: 'B0',
    24: 'C1',
    25: 'C#1',
    26: 'D1',
    27: 'D#1',
    28: 'E1',
    29: 'F1',
    30: 'F#1',
    31: 'G1',
    32: 'G#1',
    33: 'A1',
    34: 'A#1',
    35: 'B1',
    36: 'C2',
    37: 'C#2',
    38: 'D2',
    39: 'D#2',
    40: 'E2',
    41: 'F2',
    42: 'F#2',
    43: 'G2',
    44: 'G#2',
    45: 'A2',
    46: 'A#2',
    47: 'B2',
    48: 'C3',
    49: 'C#3',
    50: 'D3',
    51: 'D#3',
    52: 'E3',
    53: 'F3',
    54: 'F#3',
    55: 'G3',
    56: 'G#3',
    57: 'A3',
    58: 'A#3',
    59: 'B3',
    60: 'C4',
    61: 'C#4',
    62: 'D4',
    63: 'D#4',
    64: 'E4',
    65: 'F4',
    66: 'F#4',
    67: 'G4',
    68: 'G#4',
    69: 'A4',
    70: 'A#4',
    71: 'B4',
    72: 'C5',
    73: 'C#5',
    74: 'D5',
    75: 'D#5',
    76: 'E5',
    77: 'F5',
    78: 'F#5',
    79: 'G5',
    80: 'G#5',
    81: 'A5',
    82: 'A#5',
    83: 'B5',
    84: 'C6',
    85: 'C#6',
    86: 'D6',
    87: 'D#6',
    88: 'E6',
    89: 'F6',
    90: 'F#6',
    91: 'G6',
    92: 'G#6',
    93: 'A6',
    94: 'A#6',
    95: 'B6',
    96: 'C7',
    97: 'C#7',
    98: 'D7',
    99: 'D#7',
    100: 'E7',
    101: 'F7',
    102: 'F#7',
    103: 'G7',
    104: 'G#7',
    105: 'A7',
    106: 'A#7',
    107: 'B7',
    108: 'C8'
}
computer_should_record = True
init = False
init_time = None
time_since_last_pedal = None
time_pedal_is_down = None
time_between_notes = 0.5
play_mode = False

# A message has:
#   note (key)
#   velocity (volume)

note_queue = []
chord_progression = []  # list of note_queues

def handle_message(message):
    """
    Handles control when the computer recieves a MIDI input.

    message: mido.Message
    """
    global note_queue
    global chord_progression
    global computer_should_record
    global init
    global init_time
    global time_since_last_pedal
    global time_pedal_is_down
    global play_mode

    if message.type == 'note_on':
        if computer_should_record and message.velocity > 1:
            print("in  << %s (%s) at velocity %s" % (notes[message.note], message.note, message.velocity))
            message.velocity = message.velocity - 30
            if not note_queue:
                note_queue.insert(0, calc_octave_down(message))
            else:
                for note in note_queue:
                    if note.note != message.note and not play_mode:
                        note_queue.insert(0, message)
                        break

    elif message.type == 'control_change':
        # print("Pedal on" if message.value == 127 else "Pedal off" )
        if not init:
            init = True
            time_since_last_pedal = time.time()
            time_pedal_is_down = time.time()
        else:
            # If the pedal is double tapped, we should clear the queue.
            if message.value == 127:
                time_pedal_is_down = time.time()
                if play_mode:
                    print('Switching chords!')
                    chord_progression.insert(0, chord_progression.pop())
                    note_queue = chord_progression[-1]
                if time_since_last_pedal + 0.1 >= time.time():
                    print('double tap! clearing note_queue and chord_progression.')
                    note_queue = []
                    chord_progression = []
                    time_since_last_pedal = time.time()
                    return
                print('computer should record.')
                computer_should_record = True
                time_since_last_pedal = time.time()
            else:
                if not play_mode:
                    if time.time() >= time_pedal_is_down + 5.0:
                        print('entering play mode')
                        chord_progression.insert(0, note_queue)
                        play_mode = True
                        print('>>>> chord_progression >>>>')
                        for i, chord in enumerate(chord_progression):
                            print(i)
                            for note in chord:
                                print("\t", notes[note.note])
                            print("")
                        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                        note_queue = chord_progression[-1]
                    elif time.time() >= time_pedal_is_down + 2.50:
                        print('was held! adding note_queue to chord_progression.')
                        chord_progression.insert(0, note_queue)
                        note_queue = []
                        return
                    print('computer should not record.')
                    computer_should_record = False
                    time_since_pedal_released = time.time()
                else:
                    pass


input_name = mido.get_input_names()[0]
input_port = mido.open_input(input_name, callback=handle_message)

output_name = mido.get_output_names()[0]
output_port = mido.open_output(output_name)

def main():
    global note_queue
    global input_port
    global output_port
    global computer_should_record
    global init_time
    global last_time

    while not init:
        time.sleep(0.1)

    init_time = time.time()
    print("Record!")

    while not play_mode:
        time.sleep(0.1)

    print("Play!")

    while True:
        time.sleep(0.25)
        try:
            if note_queue:
                if time.time() >= note_queue[-1].time:
                    for msg in note_queue:
                        # msg = note_queue.pop()
                        # print("out << %s (%s) at velocity %s" % (notes[msg.note], msg.note, msg.velocity))
                        output_port.send(msg)
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
