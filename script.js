const cells = document.querySelectorAll('[data-cell]');
const resetButton = document.getElementById('resetButton');
const startButton = document.getElementById('startButton');
const nameInput = document.getElementById('player-name');
const nameContainer = document.getElementById('name-container');
const gameBoard = document.querySelector('.board');
let isXTurn = true;

startButton.addEventListener('click', startGame);
resetButton.addEventListener('click', handleReset); // Changed to handleReset

function startGame() {
    const playerName = nameInput.value.trim();
    if (playerName) {
        nameContainer.style.display = 'none';
        gameBoard.style.display = 'grid';
        resetButton.style.display = 'inline-block';
        addCellClickListeners();
    } else {
        alert('Please enter your name to start the game.');
    }
}

// New function to add click listeners to cells
function addCellClickListeners() {
    cells.forEach(cell => {
        // Remove any existing listeners first
        cell.removeEventListener('click', handleClick);
        // Add new listener
        cell.addEventListener('click', handleClick, { once: true });
    });
}

function handleClick(e) {
    const cell = e.target;
    const cellId = cell.id;
    
    // Only proceed if the cell is empty
    if (cell.textContent === '') {
        cell.textContent = isXTurn ? 'X' : 'O';
        
        fetch('http://localhost:5002/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cellId: cellId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.computerMove !== undefined) {
                const computerCell = document.getElementById(data.computerMove);
                if (computerCell && computerCell.textContent === '') {
                    computerCell.textContent = 'O';
                    computerCell.removeEventListener('click', handleClick);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function handleReset() {
    // Reset frontend game state
    isXTurn = true;
    cells.forEach(cell => {
        cell.textContent = '';
    });
    
    // Add fresh click listeners to all cells
    addCellClickListeners();
    
    // Reset backend game state
    fetch('http://localhost:5002/reset', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            console.log('Game reset');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Remove the unused resetGame function since we're using handleReset