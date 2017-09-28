import mido
from time import sleep


names = mido.get_output_names()
print(names)
output = mido.open_output(names[0])

for i in range(60,70):
    output.send(mido.Message('note_on', note=i, velocity=64))
    sleep(1)
    output.send(mido.Message('note_off', note=i, velocity=0))