import tkinter as tk
# Import tkinter library to create GUI (window, canvas, shapes)

# -----------------------------
# WINDOW SIZE
# -----------------------------
W, H = 500, 400
# W = width of the window
# H = height of the window

# -----------------------------
# CREATE MAIN WINDOW
# -----------------------------
root = tk.Tk()
root.title("Block Breaker")
# Tk() creates the main application window
# title() sets the name of the window

# -----------------------------
# CREATE CANVAS (GAME AREA)
# -----------------------------
canvas = tk.Canvas(root, width=W, height=H, bg="black")
canvas.pack()
# Canvas is the area where the game runs
# Think of it as the playground

# -----------------------------
# CREATE PADDLE
# -----------------------------
paddle = canvas.create_rectangle(
    200, 360, 300, 375, fill="white"
)
# Rectangle shape = paddle
# Placed near the bottom of the window
# Player controls this paddle

# -----------------------------
# CREATE BALL
# -----------------------------
ball = canvas.create_oval(
    240, 180, 260, 200, fill="red"
)
# Oval shape = ball

dx, dy = 4, -4
# dx = horizontal speed of the ball
# dy = vertical speed of the ball
# Positive value = right/down
# Negative value = left/up

# -----------------------------
# CREATE BRICKS
# -----------------------------
bricks = []
# List to store all bricks

for i in range(5):
    brick = canvas.create_rectangle(
        80*i + 40, 40, 80*i + 110, 60, fill="blue"
    )
    bricks.append(brick)
# Loop creates 5 bricks
# Bricks are stored in a list so we can remove them later

# -----------------------------
# SCORE SYSTEM
# -----------------------------
score = 0
# Initial score

score_text = canvas.create_text(
    250, 20, text="Score: 0", fill="white"
)
# Displays score on the screen

# -----------------------------
# PADDLE MOVEMENT (KEYBOARD)
# -----------------------------
def left(event):
    # Move paddle left when left arrow is pressed
    canvas.move(paddle, -20, 0)
    # -20 = move left, 0 = no vertical movement

def right(event):
    # Move paddle right when right arrow is pressed
    canvas.move(paddle, 20, 0)
    # 20 = move right

# Bind keyboard keys to functions
root.bind("<Left>", left)
root.bind("<Right>", right)

# -----------------------------
# GAME LOOP FUNCTION
# -----------------------------
def game():
    global dx, dy, score
    # Use global variables inside function

    # -------------------------
    # MOVE BALL
    # -------------------------
    canvas.move(ball, dx, dy)
    # Move ball slightly every time game() runs

    # Get current positions
    b = canvas.coords(ball)
    p = canvas.coords(paddle)

    # -------------------------
    # WALL COLLISION
    # -------------------------
    if b[0] <= 0 or b[2] >= W:
        dx = -dx
        # Reverse direction if ball hits left or right wall

    if b[1] <= 0:
        dy = -dy
        # Reverse direction if ball hits top wall

    # -------------------------
    # PADDLE COLLISION
    # -------------------------
    if (
        b[2] >= p[0] and
        b[0] <= p[2] and
        b[3] >= p[1]
    ):
        dy = -dy
        # Ball bounces back when it hits paddle

    # -------------------------
    # BRICK COLLISION
    # -------------------------
    for brick in bricks[:]:
        r = canvas.coords(brick)

        if (
            b[2] >= r[0] and
            b[0] <= r[2] and
            b[1] <= r[3]
        ):
            canvas.delete(brick)
            # Remove brick from screen

            bricks.remove(brick)
            # Remove brick from list

            dy = -dy
            # Ball changes direction

            score += 1
            # Increase score

            canvas.itemconfig(
                score_text, text=f"Score: {score}"
            )
            break
            # Stop checking after one collision

    # -------------------------
    # GAME OVER CONDITION
    # -------------------------
    if b[3] > H:
        canvas.create_text(
            250, 200,
            text="GAME OVER",
            fill="red",
            font=("Arial", 20)
        )
        return
        # Stop the game loop

    # -------------------------
    # CALL GAME AGAIN
    # -------------------------
    root.after(20, game)
    # Calls game() after 20 milliseconds
    # This creates animation

# -----------------------------
# START GAME
# -----------------------------
game()
# Start the game loop

root.mainloop()
# Keeps the window open
