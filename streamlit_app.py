import streamlit as st

st.set_page_config(page_title="Block Breaker Game", layout="centered")

# HTML and CSS for the game
game_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { text-align: center; }
    canvas { border: 1px solid #000; background-color: #000; }
    #score { font-size: 24px; }
  </style>
</head>
<body>
  <h1>Block Breaker Game</h1>
  <canvas id="gameCanvas" width="600" height="400"></canvas>
  <div id="score">Score: 0</div>
  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    let paddleHeight = 10;
    let paddleWidth = 75;
    let paddleX = (canvas.width - paddleWidth) / 2;

    let ballRadius = 10;
    let x = canvas.width / 2;
    let y = canvas.height - 30;
    let dx = 2;
    let dy = -2;

    const brickRowCount = 5;
    const brickColumnCount = 9;
    const brickWidth = 60;
    const brickHeight = 20;
    const brickPadding = 10;
    const brickOffsetTop = 30;
    const brickOffsetLeft = 30;

    let bricks = [];
    for(let c = 0; c < brickColumnCount; c++) {
      bricks[c] = [];
      for(let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
      }
    }

    let score = 0;

    document.addEventListener("keydown", keyDownHandler);
    document.addEventListener("keyup", keyUpHandler);

    let rightPressed = false;
    let leftPressed = false;

    function keyDownHandler(e) {
      if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = true;
      } else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = true;
      }
    }

    function keyUpHandler(e) {
      if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = false;
      } else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = false;
      }
    }

    function drawBall() {
      ctx.beginPath();
      ctx.arc(x, y, ballRadius, 0, Math.PI*2);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
    }

    function drawPaddle() {
      ctx.beginPath();
      ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
    }

    function drawBricks() {
      for(let c = 0; c < brickColumnCount; c++) {
        for(let r = 0; r < brickRowCount; r++) {
          if(bricks[c][r].status == 1) {
            let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
            let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
            bricks[c][r].x = brickX;
            bricks[c][r].y = brickY;
            ctx.beginPath();
            ctx.rect(brickX, brickY, brickWidth, brickHeight);
            ctx.fillStyle = "#0095DD";
            ctx.fill();
            ctx.closePath();
          }
        }
      }
    }

    function collisionDetection() {
      for(let c = 0; c < brickColumnCount; c++) {
        for(let r = 0; r < brickRowCount; r++) {
          let b = bricks[c][r];
          if(b.status == 1) {
            if(x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
              dy = -dy;
              b.status = 0;
              score++;
              document.getElementById('score').innerHTML = "Score: " + score;
              if(score == brickRowCount * brickColumnCount) {
                alert("YOU WIN, CONGRATULATIONS!");
                document.location.reload();
              }
            }
          }
        }
      }
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawBricks();
      drawBall();
      drawPaddle();
      collisionDetection();

      if(x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        dx = -dx;
      }
      if(y + dy < ballRadius) {
        dy = -dy;
      } else if(y + dy > canvas.height - ballRadius) {
        if(x > paddleX && x < paddleX + paddleWidth) {
          dy = -dy;
        } else {
          alert("GAME OVER");
          document.location.reload();
        }
      }

      if(rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += 7;
      } else if(leftPressed && paddleX > 0) {
        paddleX -= 7;
      }

      x += dx;
      y += dy;
      requestAnimationFrame(draw);
    }

    draw();
  </script>
</body>
</html>
"""

# Display the game
st.markdown(game_html, unsafe_allow_html=True)
