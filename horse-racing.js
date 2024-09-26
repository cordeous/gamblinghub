document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    let balance = parseInt(localStorage.getItem('balance')) || 1000;
    const horses = ['Red', 'Blue', 'Green', 'Yellow', 'Purple'];
    let selectedHorse = null;
    let currentBet = 100;
    
    function initGame() {
        gameContainer.innerHTML = `
            <h2>Horse Racing</h2>
            <p>Balance: $<span id="balance">${balance}</span></p>
            <div id="horse-selection"></div>
            <div id="bet-controls">
                <button id="decrease-bet">-</button>
                <span id="current-bet">$${currentBet}</span>
                <button id="increase-bet">+</button>
            </div>
            <div id="quick-bet">
                <button class="quick-bet-button" data-amount="50">$50</button>
                <button class="quick-bet-button" data-amount="100">$100</button>
                <button class="quick-bet-button" data-amount="200">$200</button>
                <button id="all-in">All In</button>
            </div>
            <button id="start-race" disabled>Start Race</button>
            <div id="race-track"></div>
            <div id="message"></div>
        `;
        
        const horseSelection = document.getElementById('horse-selection');
        horses.forEach(horse => {
            const button = document.createElement('button');
            button.textContent = horse;
            button.addEventListener('click', () => selectHorse(horse, button));
            horseSelection.appendChild(button);
        });
        
        document.getElementById('start-race').addEventListener('click', startRace);
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
        createHorses();
    }
    
    function selectHorse(horse, button) {
        selectedHorse = horse;
        document.querySelectorAll('#horse-selection button').forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
        document.getElementById('start-race').disabled = false;
    }
    
    function placeBet() {
        if (balance >= currentBet) {
            balance -= currentBet;
            updateBalance();
            displayMessage(`You bet $${currentBet} on ${selectedHorse}`);
            return true;
        } else {
            displayMessage("Not enough balance to place a bet!");
            return false;
        }
    }
    
    function startRace() {
        if (!selectedHorse) {
            displayMessage("Please select a horse first!");
            return;
        }
        if (!placeBet()) return;
        
        document.getElementById('start-race').disabled = true;
        const winner = horses[Math.floor(Math.random() * horses.length)];
        resetHorses();
        setTimeout(() => animateRace(winner), 100);
    }
    
    function resetHorses() {
        horses.forEach(horse => {
            const horseElement = document.getElementById(horse);
            horseElement.style.transition = 'none';
            horseElement.style.left = '0px';
        });
    }
    
    function animateRace(winner) {
        const raceTrack = document.getElementById('race-track');
        const finishLine = raceTrack.offsetWidth - 50; // 50 is the width of the horse

        horses.forEach(horse => {
            const horseElement = document.getElementById(horse);
            const randomTime = 3 + Math.random() * 2; // Random time between 3 and 5 seconds
            horseElement.style.transition = `left ${randomTime}s`;
            horseElement.style.left = horse === winner ? `${finishLine}px` : `${finishLine - Math.random() * 100}px`;
        });

        setTimeout(() => {
            if (selectedHorse === winner) {
                balance += 250; // Win amount
                displayMessage(`The winner is ${winner}! You won $250!`);
            } else {
                displayMessage(`The winner is ${winner}! Better luck next time!`);
            }
            updateBalance();
            document.querySelectorAll('#horse-selection button').forEach(btn => btn.classList.remove('selected'));
            selectedHorse = null;
            document.getElementById('start-race').disabled = false;
        }, 5500); // Wait for the animation to finish
    }
    
    function updateBalance() {
        document.getElementById('balance').textContent = balance;
        localStorage.setItem('balance', balance.toString());
    }

    function displayMessage(message) {
        document.getElementById('message').textContent = message;
    }

    function createHorses() {
        const raceTrack = document.getElementById('race-track');
        horses.forEach((horse, index) => {
            const horseElement = document.createElement('div');
            horseElement.id = horse;
            horseElement.className = 'horse';
            horseElement.style.backgroundColor = horse.toLowerCase();
            horseElement.style.top = `${index * 60 + 10}px`;
            raceTrack.appendChild(horseElement);
        });
    }

    function decreaseBet() {
        if (currentBet > 50) {
            currentBet -= 50;
            updateCurrentBet();
        }
    }

    function increaseBet() {
        if (currentBet < balance) {
            currentBet += 50;
            updateCurrentBet();
        }
    }

    function updateCurrentBet() {
        document.getElementById('current-bet').textContent = `$${currentBet}`;
    }

    initGame();
});