import tkinter as tk

# --------------------
# Window setup
# --------------------
WIDTH = 600
HEIGHT = 500

window = tk.Tk()
window.title("Block Breaker Game")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(False, False)

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# --------------------
# Score & Lives
# --------------------
score = 0
lives = 3

score_text = canvas.create_text(
    60, 15,
    text="Score: 0",
    fill="white",
    font=("Arial", 12)
)

lives_text = canvas.create_text(
    540, 15,
    text="Lives: 3",
    fill="white",
    font=("Arial", 12)
)

# --------------------
# Paddle
# --------------------
paddle_width = 100
paddle_height = 12
paddle_y = HEIGHT - 40

paddle = canvas.create_rectangle(
    WIDTH / 2 - paddle_width / 2,
    paddle_y,
    WIDTH / 2 + paddle_width / 2,
    paddle_y + paddle_height,
    fill="white"
)

def move_left(event):
    if canvas.coords(paddle)[0] > 0:
        canvas.move(paddle, -25, 0)

def move_right(event):
    if canvas.coords(paddle)[2] < WIDTH:
        canvas.move(paddle, 25, 0)

window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# --------------------
# Ball
# --------------------
ball_radius = 10
ball = canvas.create_oval(
    WIDTH/2 - ball_radius,
    HEIGHT/2 - ball_radius,
    WIDTH/2 + ball_radius,
    HEIGHT/2 + ball_radius,
    fill="red"
)

ball_dx = 4
ball_dy = -4
speed_increase = 0.2  # difficulty increase

# --------------------
# Bricks (Fixed within frame)
# --------------------
brick_rows = 4
brick_cols = 8
brick_height = 20
brick_gap = 5

brick_width = (WIDTH - (brick_cols + 1) * brick_gap) / brick_cols
bricks = []

def create_bricks():
    global ball_dx, ball_dy
    bricks.clear()
    canvas.delete("brick")

    for row in range(brick_rows):
        for col in range(brick_cols):
            x1 = brick_gap + col * (brick_width + brick_gap)
            y1 = 40 + row * (brick_height + brick_gap)
            x2 = x1 + brick_width
            y2 = y1 + brick_height

            brick = canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="blue",
                tags="brick"
            )
            bricks.append(brick)

    # increase difficulty each level
    ball_dx *= 1.1
    ball_dy *= 1.1

create_bricks()

# --------------------
# Reset Ball
# --------------------
def reset_ball():
    canvas.coords(
        ball,
        WIDTH/2 - ball_radius,
        HEIGHT/2 - ball_radius,
        WIDTH/2 + ball_radius,
        HEIGHT/2 + ball_radius
    )

# --------------------
# Game Loop
# --------------------
def game_loop():
    global ball_dx, ball_dy, score, lives

    canvas.move(ball, ball_dx, ball_dy)
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # Wall collision
    if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
        ball_dx = -ball_dx

    if ball_pos[1] <= 0:
        ball_dy = -ball_dy

    # Paddle collision
    if (
        ball_pos[2] >= paddle_pos[0] and
        ball_pos[0] <= paddle_pos[2] and
        ball_pos[3] >= paddle_pos[1] and
        ball_pos[3] <= paddle_pos[3]
    ):
        ball_dy = -abs(ball_dy)

    # Brick collision
    for brick in bricks[:]:
        brick_pos = canvas.coords(brick)
        if (
            ball_pos[2] >= brick_pos[0] and
            ball_pos[0] <= brick_pos[2] and
            ball_pos[3] >= brick_pos[1] and
            ball_pos[1] <= brick_pos[3]
        ):
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 1

            # increase speed slightly
            ball_dx *= 1 + speed_increase/10
            ball_dy *= 1 + speed_increase/10

            canvas.itemconfig(score_text, text=f"Score: {score}")
            break

    # Refill bricks
    if len(bricks) == 0:
        create_bricks()

    # Missed ball
    if ball_pos[3] > HEIGHT:
        lives -= 1
        canvas.itemconfig(lives_text, text=f"Lives: {lives}")
        reset_ball()
        ball_dy = -abs(ball_dy)

        if lives == 0:
            canvas.create_text(
                WIDTH/2, HEIGHT/2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 28, "bold")
            )
            return

    window.after(20, game_loop)

game_loop()
window.mainloop()
