import mido
import time

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
computer_should_play = True
init = False
init_time = None
last_time = None

# A message has:
#   note (key)
#   velocity (volume)

note_queue = []


def print_message(message):
    """
    Handles control when the computer recieves a MIDI input.

    message: mido.Message
    """
    global note_queue
    global computer_should_play
    global init
    global init_time
    global last_time

    if message.type == 'note_on':
        if computer_should_play:
            print("in  << %s (%s) at velocity %s" % (notes[message.note], message.note ,message.velocity))
            note_queue.insert(0, calc_octave_down(message))

    elif message.type == 'control_change':
        # print("Pedal on" if message.value == 127 else "Pedal off" )
        if not init:
            init = True
        else:
            if message.value == 127:
                computer_should_play = False
                note_queue = []
                print('computer should not play.')
            else:
                print('computer should play.')
                computer_should_play = True




input_name = mido.get_input_names()[0]
input_port = mido.open_input(input_name, callback=print_message)

output_name = mido.get_output_names()[0]
output_port = mido.open_output(output_name)

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

def calc_octave_down(msg):
    """
    Returns a note that is an octave down from the note that is input.

    msg: mido.Message
    """
    new_note = 0
    if msg.note < 33:
        new_note = msg.note
    else:
        new_note = msg.note - 12
    return mido.Message('note_on', note=new_note, velocity=msg.velocity, time=time.time() + 0.75)


def main():
    global note_queue
    global input_port
    global output_port
    global computer_should_play
    global init_time
    global last_time

    while not init:
        time.sleep(0.1)

    init_time = time.time()
    print("Play!")

    while True:
        time.sleep(0.01)
        try:
            if note_queue and computer_should_play:
                if time.time() >= note_queue[-1].time:
                    msg = note_queue.pop()
                    print("out << %s (%s) at velocity %s" % (notes[msg.note], msg.note, msg.velocity))
                    output_port.send(msg)
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
