import cv2
import sys

if len(sys.argv) != 2:
    print("invalid arguments! argument should be file path!")

reached_end = False

dot_pos = (0, 0)
dot_dir = 180
dot_val = 0

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % (rgb[2], rgb[1], rgb[0])


def hex_to_rgb(hexa):
    if len(hexa) < 6:
        hexa = '0'*(6-len(hexa)) + hexa
    return tuple(int(hexa[i:i+2], 16) for i in (0, 2, 4))


def get_at(pos):
    val = img[pos[1]][pos[0]]
    return rgb_to_hex((val[0], val[1], val[2]))


def set_at(pos, val):
    img[pos[1]][pos[0]] = hex_to_rgb(hex(val).replace("0x", ""))


def is_wall(pos):
    return get_at(pos) == '000000'


def move(amount):
    global dot_pos
    global dot_dir

    dot_pos = pos_infront(amount, dot_dir)


def wrap_dir(dir):
    return dir % 360


def pos_infront(amount, direction):
    global dot_pos

    if direction == 180:
        return (dot_pos[0] - amount, dot_pos[1])
    if direction == 0:
        return (dot_pos[0] + amount, dot_pos[1])
    if direction == 90:
        return (dot_pos[0], dot_pos[1] + amount)
    if direction == 270:
        return (dot_pos[0], dot_pos[1] - amount)


start = (0, 0)

for y, ya in enumerate(img):
    for x, xa in enumerate(ya):
        val = rgb_to_hex((xa[0], xa[1], xa[2]))
        if val == '00ff00':
            start = (x, y)

dot_pos = start

debug_max_instructions = -1

noops = 0
storage_mark = False

while not reached_end:
    # run instructions
    current = get_at(dot_pos)
    current_val = int(current, 16)
    notInstruction = False

    print("Executing " + current + " = "+str(current_val))

    if current == '00ff00':    # start
        pass
    elif current == 'ff0000':  # exit
        reached_end = True
        break
    elif current == 'ffffff':  # noop
        noops += 1
    elif current == '0000ff':  # output
        print(dot_val)
    elif current == '4800ff':  # output as char
        print(chr(dot_val))
    elif current == 'ffd800':  # store at next possible pos
        storage_mark = True
    elif current == '0094ff':  # input
        inp = input()
        if len(inp) > 0:
            dot_val = ord(inp[0])
    elif current == '7fff8e':  # clears the value of the dot (sets to 0)
        dot_val = 0

    elif current == 'ff7f7f':  # bre
        cval = 0
        succesDir = dot_dir

        vright = get_at(pos_infront(1, wrap_dir(dot_dir + 90)))
        vleft = get_at(pos_infront(1, wrap_dir(dot_dir - 90)))

        if vright == 'ffffff':
            cval = vleft
            succesDir = wrap_dir(dot_dir + 90)
        if vleft == 'ffffff':
            cval = vright
            succesDir = wrap_dir(dot_dir - 90)

        cval = int(cval, 16)

        if dot_val == cval:
            dot_dir = succesDir

    elif current == '3f7f47':  # add
        oval = 0

        vright = get_at(pos_infront(1, wrap_dir(dot_dir + 90)))
        vleft = get_at(pos_infront(1, wrap_dir(dot_dir - 90)))

        if vright == '000000':
            oval = vleft
        if vleft == '000000':
            oval = vright

        oval = int(oval, 16)

        dot_val += oval

    elif current == '9b3cb5':  # sub
        oval = 0

        vright = get_at(pos_infront(1, wrap_dir(dot_dir + 90)))
        vleft = get_at(pos_infront(1, wrap_dir(dot_dir - 90)))

        if vright == '000000':
            oval = vleft
        if vleft == '000000':
            oval = vright

        oval = int(oval, 16)

        dot_val -= oval

    elif current == 'e1cfdb':  # mul
        oval = 0

        vright = get_at(pos_infront(1, wrap_dir(dot_dir + 90)))
        vleft = get_at(pos_infront(1, wrap_dir(dot_dir - 90)))

        if vright == '000000':
            oval = vleft
        if vleft == '000000':
            oval = vright

        oval = int(oval, 16)

        dot_val *= oval

    else:                      # normal number pixel
        notInstruction = True
        dot_val += current_val

        if storage_mark:
            storage_mark = False
            set_at(dot_pos, dot_val)

    if not notInstruction:     # self modifying program
        if dot_dir == 180 or dot_dir == 270:
            set_at(dot_pos, abs(current_val + dot_val))

        if dot_dir == 0 or dot_dir == 90:
            set_at(dot_pos, abs(current_val - dot_val))

    if current != 'ffffff':
        noops -= .75

    # rotate
    if is_wall(pos_infront(1, dot_dir)):
        isWallRight = is_wall(pos_infront(1, wrap_dir(dot_dir + 90)))
        isWallLeft = is_wall(pos_infront(1, wrap_dir(dot_dir - 90)))

        if isWallRight and isWallLeft:
            dot_dir = wrap_dir(dot_dir - 180)
        elif isWallRight:  # right
            dot_dir = wrap_dir(dot_dir + 90)
        elif isWallLeft:  # left
            dot_dir = wrap_dir(dot_dir - 90)
        else:
            dot_dir = wrap_dir(dot_dir - 180)

    # move
    move(1)

    if not debug_max_instructions == -1:
        debug_max_instructions -= 1

        if debug_max_instructions <= 0:
            print("exited because of debug limitation")
            break

    if noops > 2:
        print(str(noops) + " too many noops!")
        break
