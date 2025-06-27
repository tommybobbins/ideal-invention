import time
import random
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
import qrcode

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()


width = display.get_width()
height = display.get_height()
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()

# We're creating 100 balls with their own individual colour and 1 BG colour
# for a total of 101 colours, which will all fit in the custom 256 entry palette!


class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen


# initialise shapes
balls = []
for _i in range(100):
    r = random.randint(0, 10) + 3
    balls.append(
        Ball(
            random.randint(r, r + (WIDTH - 2 * r)),
            random.randint(r, r + (HEIGHT - 2 * r)),
            r,
            (14 - r) / 2,
            (14 - r) / 2,
            display.create_pen(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        )
    )

BG = display.create_pen(40, 40, 40)

while True:
    display.set_pen(BG)
    display.clear()

    for ball in balls:
        ball.x += ball.dx
        ball.y += ball.dy

        xmax = WIDTH - ball.r
        xmin = ball.r
        ymax = HEIGHT - ball.r
        ymin = ball.r

        if ball.x < xmin or ball.x > xmax:
            ball.dx *= -1

        if ball.y < ymin or ball.y > ymax:
            ball.dy *= -1

        display.set_pen(ball.pen)
        display.circle(int(ball.x), int(ball.y), int(ball.r))

    display.update()
    time.sleep(0.01)

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(255, 255, 255)
    display.rectangle(ox, oy, size, size)
    display.set_pen(0, 0, 0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

code = qrcode.QRCode()
code.set_text("E50CD22A")
size, module_size = measure_qr_code(height, code)
left = int((width // 2) - (size // 2))
top = int((height // 2) - (size // 2))

class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

class Rect:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

# initialise shapes
balls = []
rects = []
for i in range(0, 50):
    r = random.randint(0, 10) + 3
    balls.append(
        Ball(
            random.randint(r, r + (width - 2 * r)),
            random.randint(r, r + (height - 2 * r)),
            r,
            (14 - r) / 2,
            (14 - r) / 2,
            display.create_pen(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        )
    )

for i in range(0, 50):
    r = random.randint(0, 10) + 3
    rects.append(
        Rect(
            random.randint(r, r + (width - 2 * r)),
            random.randint(r, r + (height - 2 * r)),
            r,
            (14 - r) / 2,
            (14 - r) / 2,
            display.create_pen(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        )
    )



while True:

    if display.is_pressed(display.BUTTON_A):              # if a button press is detected then...
        clear()                                           # clear to black
        display.set_pen(255, 61, 130)                    # change the pen colour
        display.text("Hi Dave", 2, 2, 240, 4)  # display some text on the screen
        display.update()                                  # update the display
        utime.sleep(1)                                    # pause for a sec
        clear()                                           # clear to black again
    elif display.is_pressed(display.BUTTON_B):
        clear()
        display.set_pen(255, 217, 033)
        display.text("Another Button", 2, 2, 240, 4)
        display.update()
        utime.sleep(1)
        clear()
    elif display.is_pressed(display.BUTTON_X):
        clear()
        display.set_pen(115, 245, 145)
        display.text("Stop pressing Buttons", 2, 2, 240, 4)
        display.update()
        utime.sleep(1)
        clear()
    elif display.is_pressed(display.BUTTON_Y):
        clear()
        display.set_pen(042, 068, 212)
        display.rectangle(0, 0, width, height )
        draw_qr_code(left, top, height, code)
        display.update()
        utime.sleep(10)
        clear()
    else:
  # this number is how frequently the Pico checks for button presses

        display.set_pen(40, 40, 40)
        display.clear()

        for ball in balls:
            ball.x += ball.dx
            ball.y += ball.dy

            xmax = width - ball.r
            xmin = ball.r
            ymax = height - ball.r
            ymin = ball.r

            if ball.x < xmin or ball.x > xmax:
                ball.dx *= -1

            if ball.y < ymin or ball.y > ymax:
                ball.dy *= -1
                
            display.set_pen(ball.pen)
            display.circle(int(ball.x), int(ball.y), int(ball.r))
                
        for rect in rects:
            rect.x += rect.dx
            rect.y += rect.dy

            xmax = width - rect.r
            xmin = rect.r
            ymax = height - rect.r
            ymin = rect.r

            if rect.x < xmin or rect.x > xmax:
                rect.dx *= -1

            if rect.y < ymin or rect.y > ymax:
                rect.dy *= -1

            display.set_pen(rect.pen)
            display.rectangle(int(rect.x), int(rect.y), int(rect.r), int(rect.r))


        display.update()
        time.sleep(0.01)