import tkinter as tk
import os
# tkinter → used to create GUI (window, canvas, shapes)
# os → used to work with files (for high score)

# =============================
# WINDOW SETTINGS
# =============================
WIDTH = 600
HEIGHT = 500
# Width and height of game window

window = tk.Tk()
window.title("Block Breaker")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(False, False)
# Creates fixed-size window

# =============================
# CANVAS (GAME AREA)
# =============================
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()
# Canvas is the playground where everything happens

# =============================
# HIGH SCORE FILE
# =============================
HIGHSCORE_FILE = "highscore.txt"
# File where highest score is saved

def load_highscore():
    # Reads high score from file
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_highscore(score):
    # Saves high score to file
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_highscore()

# =============================
# GAME STATE VARIABLES
# =============================
score = 0          # Player score
lives = 3          # Total lives
game_over = False  # Game running status

# =============================
# DISPLAY TEXT (UI)
# =============================
score_text = canvas.create_text(
    60, 15, text="Score: 0", fill="white", font=("Arial", 12)
)

high_score_text = canvas.create_text(
    WIDTH//2, 15, text=f"High Score: {high_score}",
    fill="yellow", font=("Arial", 12)
)

lives_text = canvas.create_text(
    WIDTH-60, 15, text="Lives: 3", fill="white", font=("Arial", 12)
)

# =============================
# CREATE PADDLE
# =============================
paddle_width = 100
paddle_height = 12
paddle_y = HEIGHT - 40
# Paddle stays near bottom

paddle = canvas.create_rectangle(
    WIDTH//2 - paddle_width//2,
    paddle_y,
    WIDTH//2 + paddle_width//2,
    paddle_y + paddle_height,
    fill="white"
)

# Paddle movement functions
def move_left(event):
    # Moves paddle left
    if not game_over and canvas.coords(paddle)[0] > 0:
        canvas.move(paddle, -25, 0)

def move_right(event):
    # Moves paddle right
    if not game_over and canvas.coords(paddle)[2] < WIDTH:
        canvas.move(paddle, 25, 0)

# Bind keyboard keys
window.bind("<Left>", move_left)
window.bind("<Right>", move_right)

# =============================
# CREATE BALL
# =============================
ball_radius = 10

ball = canvas.create_oval(
    WIDTH//2 - ball_radius,
    HEIGHT//2 - ball_radius,
    WIDTH//2 + ball_radius,
    HEIGHT//2 + ball_radius,
    fill="red"
)

# Ball speed variables
ball_dx = 4   # Horizontal speed
ball_dy = -4  # Vertical speed (negative = upward)

# =============================
# CREATE BRICKS
# =============================
brick_rows = 4
brick_cols = 8
brick_height = 20
brick_gap = 5

# Calculate brick width so bricks stay inside window
brick_width = (WIDTH - (brick_cols + 1) * brick_gap) / brick_cols

bricks = []
brick_speed = 0.0
# brick_speed = 0 → bricks are static (do not move)

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
                x1, y1, x2, y2, fill="blue", tags="brick"
            )
            bricks.append(brick)

    # Increase difficulty each level
    ball_dx *= 1.1
    ball_dy *= 1.1

create_bricks()

# =============================
# RESET BALL POSITION
# =============================
def reset_ball():
    canvas.coords(
        ball,
        WIDTH//2 - ball_radius,
        HEIGHT//2 - ball_radius,
        WIDTH//2 + ball_radius,
        HEIGHT//2 + ball_radius
    )

# =============================
# RESET FULL GAME (RETRY)
# =============================
def reset_game():
    global score, lives, game_over, ball_dx, ball_dy

    score = 0
    lives = 3
    game_over = False

    ball_dx = 4
    ball_dy = -4

    canvas.itemconfig(score_text, text="Score: 0")
    canvas.itemconfig(lives_text, text="Lives: 3")

    canvas.delete("game_over")
    canvas.delete("retry")

    reset_ball()
    create_bricks()
    game_loop()

def retry_game(event):
    # Retry when R is pressed
    if game_over:
        reset_game()

window.bind("r", retry_game)
window.bind("R", retry_game)

# =============================
# MAIN GAME LOOP
# =============================
def game_loop():
    global ball_dx, ball_dy, score, lives, game_over, high_score

    if game_over:
        return

    # Move ball
    canvas.move(ball, ball_dx, ball_dy)

    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)

    # -------------------------
    # WALL COLLISION
    # -------------------------
    if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
        ball_dx = -ball_dx

    if ball_pos[1] <= 0:
        ball_dy = -ball_dy

    # -------------------------
    # PADDLE COLLISION
    # -------------------------
    if (
        ball_pos[2] >= paddle_pos[0] and
        ball_pos[0] <= paddle_pos[2] and
        ball_pos[3] >= paddle_pos[1]
    ):
        ball_dy = -abs(ball_dy)

    # -------------------------
    # BRICK COLLISION
    # -------------------------
    for brick in bricks[:]:
        brick_pos = canvas.coords(brick)

        if (
            ball_pos[2] >= brick_pos[0] and
            ball_pos[0] <= brick_pos[2] and
            ball_pos[3] >= brick_pos[1]
        ):
            canvas.delete(brick)
            bricks.remove(brick)

            ball_dy = -ball_dy
            score += 1

            canvas.itemconfig(score_text, text=f"Score: {score}")
            break

    # -------------------------
    # NEXT LEVEL (INFINITE)
    # -------------------------
    if len(bricks) == 0:
        create_bricks()

    # -------------------------
    # BALL MISSED → LOSE LIFE
    # -------------------------
    if ball_pos[3] > HEIGHT:
        lives -= 1
        canvas.itemconfig(lives_text, text=f"Lives: {lives}")
        reset_ball()
        ball_dy = -abs(ball_dy)

        if lives == 0:
            game_over = True

            # Update high score
            if score > high_score:
                high_score = score
                save_highscore(high_score)
                canvas.itemconfig(
                    high_score_text,
                    text=f"High Score: {high_score}"
                )

            canvas.create_text(
                WIDTH//2, HEIGHT//2 - 20,
                text="GAME OVER",
                fill="red",
                font=("Arial", 28, "bold"),
                tags="game_over"
            )

            canvas.create_text(
                WIDTH//2, HEIGHT//2 + 20,
                text="Press R to Retry",
                fill="white",
                font=("Arial", 14),
                tags="retry"
            )
            return

    # Repeat game loop
    window.after(20, game_loop)

# =============================
# START GAME
# =============================
game_loop()
window.mainloop()
