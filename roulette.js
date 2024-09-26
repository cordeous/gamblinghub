document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    let balance = parseInt(localStorage.getItem('balance')) || 1000;
    
    function initGame() {
        gameContainer.innerHTML = `
            <h2>Roulette</h2>
            <p>Balance: $<span id="balance">${balance}</span></p>
            <div id="bet-options">
                <button class="bet-button" data-bet="red">Red ($50)</button>
                <button class="bet-button" data-bet="black">Black ($50)</button>
                <button class="bet-button" data-bet="even">Even ($50)</button>
                <button class="bet-button" data-bet="odd">Odd ($50)</button>
            </div>
            <div id="quick-bet">
                <button class="quick-bet-button" data-amount="10">$10</button>
                <button class="quick-bet-button" data-amount="50">$50</button>
                <button class="quick-bet-button" data-amount="100">$100</button>
                <button id="all-in">All In</button>
            </div>
            <div id="roulette-wheel">
                <div id="wheel"></div>
                <div id="ball"></div>
            </div>
            <div id="message"></div>
        `;
        
        createWheel();
        
        document.querySelectorAll('.bet-button').forEach(button => {
            button.addEventListener('click', () => placeBet(button.dataset.bet, 50));
        });

        document.querySelectorAll('.quick-bet-button').forEach(button => {
            button.addEventListener('click', () => {
                const amount = parseInt(button.dataset.amount);
                placeBet('quick', amount);
            });
        });

        document.getElementById('all-in').addEventListener('click', () => {
            placeBet('all-in', balance);
        });
    }
    
    function createWheel() {
        const wheel = document.getElementById('wheel');
        const numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26];
        numbers.forEach((number, index) => {
            const slice = document.createElement('div');
            slice.className = 'slice';
            slice.style.transform = `rotate(${index * 360 / 37}deg)`;
            slice.innerHTML = `<span style="transform: rotate(${-index * 360 / 37}deg)">${number}</span>`;
            if (number === 0) {
                slice.style.backgroundColor = '#0f0';
            } else if ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(number)) {
                slice.style.backgroundColor = '#f00';
            } else {
                slice.style.backgroundColor = '#000';
            }
            wheel.appendChild(slice);
        });
    }
    
    function placeBet(betType, bet) {
        if (balance >= bet) {
            balance -= bet;
            updateBalance();
            spinWheel(betType, bet);
        } else {
            displayMessage("Not enough balance to place a bet!");
        }
    }
    
    function spinWheel(betType, bet) {
        const wheel = document.getElementById('wheel');
        const ball = document.getElementById('ball');
        const spins = 5 + Math.random() * 5;
        const duration = 5000 + Math.random() * 2000;
        const wheelRotation = 360 * spins;
        const ballRotation = 360 * (spins + 1 + Math.random());

        wheel.style.transition = `transform ${duration}ms cubic-bezier(0.25, 0.1, 0.25, 1)`;
        ball.style.transition = `transform ${duration}ms cubic-bezier(0.25, 0.1, 0.25, 1)`;
        
        requestAnimationFrame(() => {
            wheel.style.transform = `rotate(${wheelRotation}deg)`;
            ball.style.transform = `rotate(${ballRotation}deg)`;
        });
        
        setTimeout(() => {
            const result = Math.floor(Math.random() * 37);
            const isWin = checkWin(betType, result);
            if (isWin) {
                balance += bet * 2;
                displayMessage(`You won! The number was ${result}.`);
            } else {
                displayMessage(`You lost. The number was ${result}.`);
            }
            updateBalance();
            
            // Reset wheel and ball position
            wheel.style.transition = 'none';
            ball.style.transition = 'none';
            requestAnimationFrame(() => {
                wheel.style.transform = `rotate(${wheelRotation % 360}deg)`;
                ball.style.transform = `rotate(${ballRotation % 360}deg)`;
            });
        }, duration);
    }
    
    function checkWin(betType, result) {
        if (betType === 'red' && [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(result)) return true;
        if (betType === 'black' && [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35].includes(result)) return true;
        if (betType === 'even' && result % 2 === 0 && result !== 0) return true;
        if (betType === 'odd' && result % 2 !== 0) return true;
        return false;
    }
    
    function updateBalance() {
        document.getElementById('balance').textContent = balance;
        localStorage.setItem('balance', balance.toString());
    }

    function displayMessage(message) {
        document.getElementById('message').textContent = message;
    }

    initGame();
});