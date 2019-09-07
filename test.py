import mido
import time

port_name = mido.get_output_names()[0]
port = mido.open_output(port_name)

for i in range(21, 107):
  msg = mido.Message('note_on', note=i, time=1, velocity=64)
  port.send(msg)
  time.sleep(0.25)
