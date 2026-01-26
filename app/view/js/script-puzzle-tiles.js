const board = document.getElementById("board");
const bank = document.querySelector("#tile-container");

const boardWidth = parseInt(document.getElementById("board-width").innerText);
const boardHeight = parseInt(document.getElementById("board-height").innerText);
const puzzleSolutionHash = document.getElementById("solution-hash").innerText;
const imageId = parseInt(document.getElementById("image-id").innerText);

let draggedItem = null;

// Gestion du Drag & Drop robuste
document.addEventListener("dragstart", (e) => {
    const tile = e.target.closest(".puzzle-tile");
    if (tile) {
        draggedItem = tile;
        e.dataTransfer.setData("text/plain", tile.id);
        setTimeout(() => tile.style.opacity = "0.5", 0);
    }
});

document.addEventListener("dragend", (e) => {
    if (draggedItem) draggedItem.style.opacity = "1";
});

document.addEventListener("dragover", (e) => {
    e.preventDefault(); // Nécessaire pour autoriser le drop
});

document.addEventListener("drop", (e) => {
    e.preventDefault();
    if (!draggedItem) return;

    const targetCell = e.target.closest(".puzzle-cell");
    const targetBank = e.target.closest("#tile-container");

    if (targetCell) {
        // Drop sur le plateau : si la cellule est déjà occupée, on échange
        if (targetCell.children.length > 0 && targetCell.children[0] !== draggedItem) {
            bank.appendChild(targetCell.children[0]);
        }
        targetCell.appendChild(draggedItem);
        checkVictory();
    } 
    else if (targetBank) {
        // Drop dans la réserve
        bank.appendChild(draggedItem);
    }
});

// Double clic pour rotation
document.addEventListener("dblclick", (e) => {
    const tile = e.target.closest(".puzzle-tile");
    if (tile) {
        const img = tile.querySelector("img");
        let currentRotation = parseInt(img.style.transform.match(/\d+/) || 0);
        let newRotation = (currentRotation + 90) % 360;
        img.style.transform = `rotate(${newRotation}deg)`;
        checkVictory();
    }
});

function checkVictory() {
    const allTiles = document.querySelectorAll(".puzzle-tile");
    const solution = getSolution(allTiles);
    
    // Le puzzle n'est fini que si toutes les pièces sont sur le plateau (ont un parent cellule)
    const tilesOnBoard = board.querySelectorAll(".puzzle-tile").length;
    
    if (tilesOnBoard === boardWidth * boardHeight) {
        if (hashSolution(solution, boardWidth) === puzzleSolutionHash) {
            console.log("Félicitations !");
            window.location.href = `/victoire?image_id=${imageId}`;
        }
    }
}

function getSolution(puzzleTilesElements) {
    let res = [];
    puzzleTilesElements.forEach(tileElement => {
        let parentCell = tileElement.closest(".puzzle-cell");
        if (parentCell) {
            let tileId = parseInt(tileElement.id.split("-")[2]);
            let cellIdData = parentCell.id.split("-"); // puzzle-cell-row-col
            let tileRow = parseInt(cellIdData[2]);
            let tileCol = parseInt(cellIdData[3]);
            let img = tileElement.querySelector("img");
            let tileRot = parseInt(img.style.transform.match(/\d+/) || 0);
            
            res.push({ "id": tileId, "row": tileRow, "col": tileCol, "rotDeg": tileRot });
        }
    });

    // Tri par ligne puis par colonne pour le hash
    res.sort((a, b) => (a.row - b.row) || (a.col - b.col));
    return res;
}

function hashSolution(solution, size) {
    const offset = 13;
    let res = "";
    for (const tileConfig of solution) {
        // Calcul du hash synchronisé avec le serveur
        let charCode = tileConfig.row * size + tileConfig.col + tileConfig.rotDeg;
        res += String.fromCharCode(charCode + offset);
    }
    return res;
}