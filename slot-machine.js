document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    let balance = 1000;
    const symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣'];
    let currentBet = 10;
    
    function initGame() {
        gameContainer.innerHTML = `
            <h2>Slot Machine</h2>
            <p>Balance: $<span id="balance">${balance}</span></p>
            <div id="slot-machine">
                <div class="reel" id="reel1"><div class="symbols"></div></div>
                <div class="reel" id="reel2"><div class="symbols"></div></div>
                <div class="reel" id="reel3"><div class="symbols"></div></div>
            </div>
            <div id="bet-controls">
                <button id="decrease-bet">-</button>
                <span id="current-bet">$${currentBet}</span>
                <button id="increase-bet">+</button>
            </div>
            <button id="spin-button">Spin</button>
            <div id="quick-bet">
                <button class="quick-bet-button" data-amount="10">$10</button>
                <button class="quick-bet-button" data-amount="50">$50</button>
                <button class="quick-bet-button" data-amount="100">$100</button>
                <button id="all-in">All In</button>
            </div>
            <div id="message"></div>
        `;
        
        document.getElementById('spin-button').addEventListener('click', () => spin(currentBet));
        document.getElementById('decrease-bet').addEventListener('click', decreaseBet);
        document.getElementById('increase-bet').addEventListener('click', increaseBet);
        document.querySelectorAll('.quick-bet-button').forEach(button => {
            button.addEventListener('click', () => {
                const amount = parseInt(button.dataset.amount);
                spin(amount);
            });
        });

        document.getElementById('all-in').addEventListener('click', () => {
            spin(balance);
        });

        initReels();
    }
    
    function initReels() {
        document.querySelectorAll('.reel .symbols').forEach(reel => {
            reel.innerHTML = Array(20).fill(0).map(() => `<div class="symbol">${symbols[Math.floor(Math.random() * symbols.length)]}</div>`).join('');
        });
    }
    
    function spin(bet) {
        if (balance >= bet) {
            balance -= bet;
            updateBalance();
            
            const results = [
                symbols[Math.floor(Math.random() * symbols.length)],
                symbols[Math.floor(Math.random() * symbols.length)],
                symbols[Math.floor(Math.random() * symbols.length)]
            ];
            
            animateReels(results);
            
            setTimeout(() => {
                checkWin(results, bet);
            }, 3000);
        } else {
            displayMessage("Not enough balance to spin!");
        }
    }
    
    function animateReels(results) {
        results.forEach((symbol, index) => {
            const reel = document.getElementById(`reel${index + 1}`);
            const symbolsContainer = reel.querySelector('.symbols');
            const symbolHeight = 100;
            const totalSpins = 20 + index * 5;
            
            symbolsContainer.style.transition = `transform ${1 + index * 0.5}s cubic-bezier(.5, 0, .5, 1)`;
            symbolsContainer.style.transform = `translateY(-${symbolHeight * totalSpins}px)`;
            
            setTimeout(() => {
                symbolsContainer.style.transition = 'none';
                symbolsContainer.style.transform = 'translateY(0)';
                symbolsContainer.innerHTML = Array(20).fill(0).map((_, i) => 
                    `<div class="symbol">${i === 0 ? symbol : symbols[Math.floor(Math.random() * symbols.length)]}</div>`
                ).join('');
            }, (1 + index * 0.5) * 1000);
        });
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
    
    function checkWin(results, bet) {
        if (results[0] === results[1] && results[1] === results[2]) {
            const winAmount = bet * 10;
            balance += winAmount;
            displayMessage(`Jackpot! You won $${winAmount}!`);
        } else if (results[0] === results[1] || results[1] === results[2] || results[0] === results[2]) {
            const winAmount = bet * 2;
            balance += winAmount;
            displayMessage(`You won $${winAmount}!`);
        } else {
            displayMessage("Better luck next time!");
        }
        updateBalance();
    }
    
    function updateBalance() {
        document.getElementById('balance').textContent = balance;
    }

    function displayMessage(message) {
        document.getElementById('message').textContent = message;
    }

    initGame();
});