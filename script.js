document.addEventListener('DOMContentLoaded', () => {
    // Initialize balance if it doesn't exist
    if (!localStorage.getItem('balance')) {
        localStorage.setItem('balance', '1000');
    }

    // Display the balance
    updateBalance();

    function updateBalance() {
        const balance = localStorage.getItem('balance');
        document.getElementById('balance').textContent = balance;
    }
});