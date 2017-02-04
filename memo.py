# implementation of card game - Memory

# Two modes: playing with numbers (beginners' level:) and playing with a pieces of pictures.
# 'Numbers' mode is standard: look for paired numbers, flipping over the unpaired.
# In 'picture' mode, there is additional functionality:
#   5 pictures are available (switch by "Restart" button)
#   and for each picture, when all the cards are exposed, the whole picture is shown with a title.

import simplegui
import random
image1 = simplegui.load_image("https://dl.dropbox.com/s/do8lyc5ifinnct8/serat.jpg")
image2 = simplegui.load_image("https://dl.dropbox.com/s/hd171gd9puvsfp2/van_gogh.jpg")
image3 = simplegui.load_image("https://dl.dropbox.com/s/6dy935nh4dk58i0/monet.jpg")
image4 = simplegui.load_image("https://dl.dropbox.com/s/mctl3x35huwulmo/pissarro.jpg")
image5 = simplegui.load_image("https://dl.dropbox.com/s/lb6njrtr19ixax2/cezanne.jpg")

gallery_lables = {image1:"Sunday afternoon on the island of La Grande-Jatte by SEURAT",
                  image2:"Night Cafe by VAN GOGH",
                  image3:"The Red Boats Argenteuil by MONET",
                  image4:"Recolte des foins by PISSARRO",
                  image5:"Compotier, Pitcher, and Fruit (Nature morte) by CEZANNE"}

pic_index = 0

# helper function to initialize globals
def init():
    """Creates a list of cards and shuffles it.
Creates a 'mirror' list of booleans to determine whether the card is exposed or not.
Initializes global variables to control the state of game and num of moves."""
    global memory_list, exposed, i, moves, state, pic, pic_index
    state = 0
    memory_list = [i % 8 for i in range(16)]       # ended with i = 15
    exposed = [0 for i in range(16)]
    random.shuffle(memory_list)
    l.set_text("Moves = 0")
    moves = 1
    name.set_text("")
    pic_index = (pic_index + 1) % 5


def init_num():
    """Initialize a global to switch to 'numbers' mode"""
    global pic
    pic = False
    init()

def init_pic():
    """Initialize a global to switch to 'picture' mode"""
    global pic, gallery
    gallery = [image1, image2, image3, image4, image5]
    pic = True
    init()

# define event handlers
def mouseclick(pos):
    """Exposes cards and compares their value.
Unpaired cards flip over again."""
    global state, compare1, compare2, moves

# To calculate index, firstly I find the number of cards' widths to the left of click's position.
# Then, if the card is in the second row, index is increased by 8.
    index = pos[0] // 50 + 8 * (pos[1] // 100)
    l.set_text("Moves = " + str(moves))
    if not exposed[index]:
        if state == 0:
            exposed[index] = True
            compare1 = index
            state = 1
        elif state == 1:
            exposed[index] = True
            compare2 = index
            state = 2
            moves += 1
        else:
            if memory_list[compare1] != memory_list[compare2]:
                exposed[compare1] = False
                exposed[compare2] = False
            exposed[index] = True
            compare1 = index
            state = 1

def draw(canvas):
    """Using i as lists' indexes and as a counter to calculate
x coordinate for drawing, draws either a card, or its 'reverse'"""
    global i, pic, pic_index, gallery
    y = 0
    for num in memory_list:
        i = (i + 1) % 16      # i turns to 0: i = (15 + 1) % 16
        x = (i % 8) * 50      # helper variable to calculate x coordinate
        y = (i // 8) * 100    # helper variable to calculate y coordinate
        if exposed[i]:
            if pic:
                # Playing with picture
                canvas.draw_image(gallery[pic_index],
                                 [memory_list[i] * 70 + 35, 170], [70, 140], [x + 25, y + 50], [50, 100])
                #      if all cards are exposed, show the picture and a title
                if False not in exposed:
                    canvas.draw_image(gallery[pic_index],
                                      [320, 160], [640, 320], [200, 100], [400, 200])
                    name.set_text(gallery_lables[gallery[pic_index]])
                # Playing with numbers
            else:
                canvas.draw_text(str(num), (x + 5, y + 75), 60, "White")
        # Drawing 'flipped cards'
        else:
            canvas.draw_polygon([(x, y), (x + 50, y), (x + 50, y + 100), (x, y + 100)], 1, "White", "Teal")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 200)
l = frame.add_label("Moves = 0")
frame.add_button("Restart", init)
frame.add_button("Play with numbers", init_num)
frame.add_button("Play with pictures", init_pic)
name = frame.add_label("")

# initialize global variables
init_num()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
