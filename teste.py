import mido
from time import sleep


names = mido.get_output_names()
print(names)
output = mido.open_output(names[2])

for i in range(60,70):
    output.send(mido.Message('control_change', control=3, value=0))
    output.send(mido.Message('note_on', note=i, velocity=64))
    # for j in range(100):
    #     output.send(mido.Message('pitchwheel',pitch = j*30))
    #     sleep(1/300.0)
    # for j in range(100):
    #     output.send(mido.Message('pitchwheel', pitch=3000 - j * 30))
    #     sleep(1 / 3000.0)
    # for j in range(100):
    #     output.send(mido.Message('pitchwheel',pitch = -j*30))
    #     sleep(1/300.0)
    # for j in range(100):
    #     output.send(mido.Message('pitchwheel', pitch=-3000 + j * 30))
    #     sleep(1 / 300.0)
    sleep(1)
    output.send(mido.Message('control_change', control=3, value=1))
    sleep(1)
    output.send(mido.Message('note_off', note=i, velocity=0))