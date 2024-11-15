// Select all cells and add click event listeners to each
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(event) {
    const cellId = event.target.id;  // Get the ID of the clicked cell
    if (!event.target.textContent) {  // Only proceed if the cell is empty
        event.target.textContent = 'X';  // Mark player's move as "X" on the board

        // Send the player's move to the backend
        fetch('http://localhost:5002/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cellId: cellId })  // Send the cellId as part of the request body
        })
        .then(response => response.json())  // Parse JSON response from backend
        .then(data => {
            const computerMove = data.computerMove;  // Get the computer's move from backend response
            if (computerMove !== null) {
                document.getElementById(computerMove).textContent = 'O';  // Mark computer's move as "O" on the board
            }
        })
        .catch(error => console.error('Error:', error));  // Log any errors to the console
    }
}
