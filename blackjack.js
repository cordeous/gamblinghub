document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    let balance = 1000;
    let playerHand = [];
    let dealerHand = [];
    let deck = [];
    let currentBet = 20;
    const suits = ['♠', '♥', '♦', '♣'];
    const values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    
    function initGame() {
        gameContainer.innerHTML = `
            <h2>Blackjack</h2>
            <p>Balance: $<span id="balance">${balance}</span></p>
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
            <div id="game-area" style="display: none;">
                <h3>Dealer's Hand: <span id="dealer-score"></span></h3>
                <div id="dealer-hand" class="hand"></div>
                <h3>Your Hand: <span id="player-score"></span></h3>
                <div id="player-hand" class="hand"></div>
                <div id="game-controls">
                    <button id="hit">Hit</button>
                    <button id="stand">Stand</button>
                </div>
            </div>
            <div id="message"></div>
        `;
        
        document.getElementById('start-game').addEventListener('click', () => startGame(currentBet));
        document.getElementById('decrease-bet').addEventListener('click', decreaseBet);
        document.getElementById('increase-bet').addEventListener('click', increaseBet);
        document.getElementById('hit').addEventListener('click', hit);
        document.getElementById('stand').addEventListener('click', stand);
        document.querySelectorAll('.quick-bet-button').forEach(button => {
            button.addEventListener('click', () => {
                const amount = parseInt(button.dataset.amount);
                startGame(amount);
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
            
            deck = createDeck();
            playerHand = [drawCard(), drawCard()];
            dealerHand = [drawCard(), drawCard()];
            
            updateHandDisplay('player', playerHand);
            updateHandDisplay('dealer', [dealerHand[0], {rank: '?', suit: '?'}]);
            updateScores();
            
            document.getElementById('game-area').style.display = 'block';
            document.getElementById('start-game').style.display = 'none';
            document.getElementById('game-controls').style.display = 'block';
            document.getElementById('message').textContent = '';
            
            checkBlackjack();
        } else {
            displayMessage("Not enough balance to start the game!");
        }
    }
    
    function createDeck() {
        return suits.flatMap(suit => values.map(value => ({rank: value, suit: suit})));
    }
    
    function drawCard() {
        return deck.splice(Math.floor(Math.random() * deck.length), 1)[0];
    }
    
    function updateHandDisplay(player, hand) {
        const handElement = document.getElementById(`${player}-hand`);
        handElement.innerHTML = hand.map(card => `<div class="card ${card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'}">${card.rank}${card.suit}</div>`).join('');
    }
    
    function updateScores() {
        document.getElementById('player-score').textContent = `(${calculateHandValue(playerHand)})`;
        const dealerScore = dealerHand.length === 2 && dealerHand[1].rank === '?' ? calculateHandValue([dealerHand[0]]) : calculateHandValue(dealerHand);
        document.getElementById('dealer-score').textContent = `(${dealerScore})`;
    }
    
    function hit() {
        playerHand.push(drawCard());
        updateHandDisplay('player', playerHand);
        updateScores();
        
        if (calculateHandValue(playerHand) > 21) {
            endGame('Player busts! Dealer wins.');
        }
    }
    
    function stand() {
        revealDealerHand();
        while (calculateHandValue(dealerHand) < 17) {
            dealerHand.push(drawCard());
            updateHandDisplay('dealer', dealerHand);
            updateScores();
        }
        
        const playerValue = calculateHandValue(playerHand);
        const dealerValue = calculateHandValue(dealerHand);
        
        if (dealerValue > 21) {
            endGame('Dealer busts! Player wins!', currentBet * 2);
        } else if (playerValue > dealerValue) {
            endGame('Player wins!', currentBet * 2);
        } else if (playerValue < dealerValue) {
            endGame('Dealer wins!');
        } else {
            endGame('It\'s a tie!', currentBet);
        }
    }
    
    function calculateHandValue(hand) {
        let value = 0;
        let aces = 0;
        
        for (let card of hand) {
            if (card.rank === 'A') {
                aces += 1;
                value += 11;
            } else if (['K', 'Q', 'J'].includes(card.rank)) {
                value += 10;
            } else if (card.rank !== '?') {
                value += parseInt(card.rank);
            }
        }
        
        while (value > 21 && aces > 0) {
            value -= 10;
            aces -= 1;
        }
        
        return value;
    }
    
    function checkBlackjack() {
        const playerValue = calculateHandValue(playerHand);
        const dealerValue = calculateHandValue(dealerHand);
        
        if (playerValue === 21 && dealerValue === 21) {
            revealDealerHand();
            endGame('Both have Blackjack! It\'s a tie!', currentBet);
        } else if (playerValue === 21) {
            revealDealerHand();
            endGame('Player has Blackjack! Player wins!', currentBet * 2.5);
        } else if (dealerValue === 21) {
            revealDealerHand();
            endGame('Dealer has Blackjack! Dealer wins!');
        }
    }
    
    function revealDealerHand() {
        updateHandDisplay('dealer', dealerHand);
        updateScores();
    }
    
    function endGame(message, payout = 0) {
        balance += payout;
        updateBalance();
        displayMessage(`${message} ${payout > 0 ? `You won $${payout}!` : ''}`);
        document.getElementById('game-controls').style.display = 'none';
        document.getElementById('start-game').style.display = 'block';
    }
    
    function updateBalance() {
        document.getElementById('balance').textContent = balance;
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