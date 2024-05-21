import streamlit as st
import time

# Initialize the game state
if 'paddle_x' not in st.session_state:
    st.session_state.paddle_x = 0.5
if 'ball_pos' not in st.session_state:
    st.session_state.ball_pos = [0.5, 0.5]
if 'ball_dir' not in st.session_state:
    st.session_state.ball_dir = [0.03, -0.03]
if 'bricks' not in st.session_state:
    st.session_state.bricks = [[x, y] for x in range(10) for y in range(5)]

def draw_game():
    canvas = st.canvas(height=400, width=600)
    
    # Draw the paddle
    paddle_width = 0.1
    paddle_height = 0.02
    canvas.rect(st.session_state.paddle_x - paddle_width/2, 0.9, paddle_width, paddle_height, color='green')
    
    # Draw the ball
    ball_radius = 0.02
    canvas.circle(st.session_state.ball_pos[0], st.session_state.ball_pos[1], ball_radius, color='white')
    
    # Draw the bricks
    brick_width = 0.1
    brick_height = 0.05
    for brick in st.session_state.bricks:
        canvas.rect(brick[0] * brick_width, brick[1] * brick_height, brick_width, brick_height, color='red')
    
    canvas.render()

def move_paddle(direction):
    paddle_speed = 0.05
    if direction == 'left':
        st.session_state.paddle_x = max(st.session_state.paddle_x - paddle_speed, 0.05)
    elif direction == 'right':
        st.session_state.paddle_x = min(st.session_state.paddle_x + paddle_speed, 0.95)

def update_ball():
    st.session_state.ball_pos[0] += st.session_state.ball_dir[0]
    st.session_state.ball_pos[1] += st.session_state.ball_dir[1]
    
    # Ball collision with walls
    if st.session_state.ball_pos[0] <= 0 or st.session_state.ball_pos[0] >= 1:
        st.session_state.ball_dir[0] = -st.session_state.ball_dir[0]
    if st.session_state.ball_pos[1] <= 0:
        st.session_state.ball_dir[1] = -st.session_state.ball_dir[1]
    
    # Ball collision with paddle
    paddle_width = 0.1
    paddle_height = 0.02
    if (0.9 <= st.session_state.ball_pos[1] <= 0.9 + paddle_height and
        st.session_state.paddle_x - paddle_width/2 <= st.session_state.ball_pos[0] <= st.session_state.paddle_x + paddle_width/2):
        st.session_state.ball_dir[1] = -st.session_state.ball_dir[1]
    
    # Ball collision with bricks
    brick_width = 0.1
    brick_height = 0.05
    new_bricks = []
    for brick in st.session_state.bricks:
        if (brick[0] * brick_width <= st.session_state.ball_pos[0] <= (brick[0] + 1) * brick_width and
            brick[1] * brick_height <= st.session_state.ball_pos[1] <= (brick[1] + 1) * brick_height):
            st.session_state.ball_dir[1] = -st.session_state.ball_dir[1]
        else:
            new_bricks.append(brick)
    st.session_state.bricks = new_bricks

st.title('Block Breaker Game')

if st.button('Start Game'):
    while len(st.session_state.bricks) > 0 and st.session_state.ball_pos[1] < 1:
        update_ball()
        draw_game()
        time.sleep(0.1)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button('Left'):
        move_paddle('left')
with col3:
    if st.button('Right'):
        move_paddle('right')

draw_game()
