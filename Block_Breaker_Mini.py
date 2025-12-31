import tkinter as tk

W, H = 500, 400

root = tk.Tk()
root.title("Block Breaker")

canvas = tk.Canvas(root, width=W, height=H, bg="black")
canvas.pack()

# Paddle
paddle = canvas.create_rectangle(200, 360, 300, 375, fill="white")

# Ball
ball = canvas.create_oval(240, 180, 260, 200, fill="red")
dx, dy = 4, -4

# Bricks
bricks = []
for i in range(5):
    brick = canvas.create_rectangle(80*i+40, 40, 80*i+110, 60, fill="blue")
    bricks.append(brick)

score = 0
score_text = canvas.create_text(250, 20, text="Score: 0", fill="white")

# Paddle movement
def left(event):
    canvas.move(paddle, -20, 0)

def right(event):
    canvas.move(paddle, 20, 0)

root.bind("<Left>", left)
root.bind("<Right>", right)

# Game loop
def game():
    global dx, dy, score

    canvas.move(ball, dx, dy)
    b = canvas.coords(ball)
    p = canvas.coords(paddle)

    # Wall collision
    if b[0] <= 0 or b[2] >= W:
        dx = -dx
    if b[1] <= 0:
        dy = -dy

    # Paddle collision
    if b[2] >= p[0] and b[0] <= p[2] and b[3] >= p[1]:
        dy = -dy

    # Brick collision
    for brick in bricks[:]:
        r = canvas.coords(brick)
        if b[2] >= r[0] and b[0] <= r[2] and b[1] <= r[3]:
            canvas.delete(brick)
            bricks.remove(brick)
            dy = -dy
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            break

    # Game over
    if b[3] > H:
        canvas.create_text(250, 200, text="GAME OVER", fill="red", font=("Arial", 20))
        return

    root.after(20, game)

game()
root.mainloop()
