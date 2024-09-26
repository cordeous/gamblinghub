document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    let balance = 1000;
    let snake = [{x: 150, y: 150}];
    let food = {};
    let direction = 'right';
    let gameLoop;
    const gridSize = 20;
    const gameSpeed = 100;
    let currentBet = 50;
    let score = 0;
    
    function initGame() {
        gameContainer.innerHTML = `
            <h2>Snake Game</h2>
            <p>Balance: $<span id="balance">${balance}</span></p>
            <p>Score: <span id="score">0</span></p>
            <div id="bet-controls">
                <button id="decrease-bet">-</button>
                <span id="current-bet">$${currentBet}</span>
                <button id="increase-bet">+</button>
            </div>
            <button id="start-game">Start Game</button>
            <div id="quick-bet">
                <button class="quick-bet-button" data-amount="10">$10</button>
                <button class="quick-bet-button" data-amount="50">$50</button>
                <button class="quick-bet-button" data-amount="100">$100</button>
                <button id="all-in">All In</button>
            </div>
            <canvas id="game-board" width="300" height="300"></canvas>
            <div id="message"></div>
        `;
        
        document.getElementById('start-game').addEventListener('click', () => startGame(currentBet));
        document.getElementById('decrease-bet').addEventListener('click', decreaseBet);
        document.getElementById('increase-bet').addEventListener('click', increaseBet);
        document.querySelectorAll('.quick-bet-button').forEach(button => {
            button.addEventListener('click', () => {
                currentBet = parseInt(button.dataset.amount);
                updateCurrentBet();
            });
        });
        
        document.getElementById('all-in').addEventListener('click', () => {
            currentBet = balance;
            updateCurrentBet();
        });
    }
    
    function startGame(bet) {
        if (balance >= bet) {
            balance -= bet;
            updateBalance();
            
            snake = [{x: 150, y: 150}];
            createFood();
            direction = 'right';
            score = 0;
            updateScore();
            
            if (gameLoop) clearInterval(gameLoop);
            gameLoop = setInterval(moveSnake, gameSpeed);
            
            document.addEventListener('keydown', changeDirection);
            document.getElementById('start-game').disabled = true;
        } else {
            displayMessage("Not enough balance to start the game!");
        }
    }
    
    function moveSnake() {
        const head = {...snake[0]};
        
        switch(direction) {
            case 'up': head.y -= gridSize; break;
            case 'down': head.y += gridSize; break;
            case 'left': head.x -= gridSize; break;
            case 'right': head.x += gridSize; break;
        }
        
        snake.unshift(head);
        
        if (head.x === food.x && head.y === food.y) {
            createFood();
            score++;
            updateScore();
        } else {
            snake.pop();
        }
        
        if (checkCollision()) {
            endGame();
        } else {
            drawGame();
        }
    }
    
    function createFood() {
        food = {
            x: Math.floor(Math.random() * (300 / gridSize)) * gridSize,
            y: Math.floor(Math.random() * (300 / gridSize)) * gridSize
        };
    }
    
    function drawGame() {
        const canvas = document.getElementById('game-board');
        const ctx = canvas.getContext('2d');
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw snake
        ctx.fillStyle = 'green';
        snake.forEach(part => {
            ctx.fillRect(part.x, part.y, gridSize - 1, gridSize - 1);
        });
        
        // Draw food
        ctx.fillStyle = 'red';
        ctx.fillRect(food.x, food.y, gridSize - 1, gridSize - 1);
    }
    
    function changeDirection(event) {
        const keyPressed = event.keyCode;
        const goingUp = direction === 'up';
        const goingDown = direction === 'down';
        const goingRight = direction === 'right';
        const goingLeft = direction === 'left';

        if (keyPressed === 37 && !goingRight) {
            direction = 'left';
        } else if (keyPressed === 38 && !goingDown) {
            direction = 'up';
        } else if (keyPressed === 39 && !goingLeft) {
            direction = 'right';
        } else if (keyPressed === 40 && !goingUp) {
            direction = 'down';
        }
    }
    
    function checkCollision() {
        const head = snake[0];
        return (
            head.x < 0 || head.x >= 300 || head.y < 0 || head.y >= 300 ||
            snake.slice(1).some(part => part.x === head.x && part.y === head.y)
        );
    }
    
    function endGame() {
        clearInterval(gameLoop);
        const winAmount = score * currentBet;
        balance += winAmount;
        updateBalance();
        displayMessage(`Game over! Your score: ${score}. You won $${winAmount}!`);
        document.getElementById('start-game').disabled = false;
    }
    
    function updateBalance() {
        document.getElementById('balance').textContent = balance;
    }

    function updateScore() {
        document.getElementById('score').textContent = score;
    }

    function displayMessage(message) {
        document.getElementById('message').textContent = message;
    }

    function decreaseBet() {
        if (currentBet > 10) {
            currentBet -= 10;
            updateCurrentBet();
        }
    }

    function increaseBet() {
        if (currentBet < balance) {
            currentBet += 10;
            updateCurrentBet();
        }
    }

    function updateCurrentBet() {
        document.getElementById('current-bet').textContent = `$${currentBet}`;
    }

    initGame();
});