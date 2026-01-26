const tileContainer = document.getElementById("tile-container");
let draggedItem = null;

const boardWidth = parseInt( document.getElementById("board-width").innerText );
const boardHeight = parseInt( document.getElementById("board-height").innerText );
const puzzleSolutionHash =  document.getElementById("solution-hash").innerText;
const imageId = parseInt( document.getElementById("image-id").innerText );

let puzzleSolved = false;


tileContainer.addEventListener("dragstart", (e) => {
	draggedItem = e.target;
});

tileContainer.addEventListener("dragover", (e) => {
	e.preventDefault();
});

tileContainer.addEventListener("drop", (e) => {
	e.preventDefault();
	const targetItem = e.target;
	if( targetItem && targetItem !== draggedItem )
	{
		if( targetItem.classList.contains("puzzle-cell"))// déplacement dans le plateau
		{
			targetItem.insertBefore(draggedItem.parentElement.parentElement, targetItem.firstElementChild);

			const solution = getSolution(puzzleTiles);
			console.log(`solution : ${solution}`);
			if( solution.length === boardWidth * boardHeight && hashSolution(solution, boardWidth) === puzzleSolutionHash ) {
				console.log("le puzzle est fini");
				puzzleSolved = true;
				window.location.href = `/victoire?image_id=${imageId}`

			}
		}
		else if( targetItem.parentElement.parentElement.classList.contains("puzzle-tile") ) {// inversion avec une autre tuile
			const draggedIndex = [...tileContainer.children].indexOf(draggedItem.parentElement.parentElement);
			const targetIndex = [...tileContainer.children].indexOf(targetItem.parentElement.parentElement);
			if (draggedIndex < targetIndex) {
				tileContainer.insertBefore(draggedItem.parentElement.parentElement, targetItem.parentElement.parentElement.nextSibling);
			}
			else {
				tileContainer.insertBefore(draggedItem.parentElement.parentElement, targetItem.parentElement.parentElement);
			}
		}
		else {// déplacement hors du plateau
			tileContainer.insertBefore(draggedItem.parentElement.parentElement, tileContainer.children[1]);
		}
	}
});


const puzzleTiles = [];
for( const containerChild of tileContainer.children[1].children){
	if( containerChild.classList.contains("puzzle-tile") ){
		puzzleTiles.push(containerChild);
	}
}

for( puzzleTile of puzzleTiles )
{
	puzzleTile.addEventListener("dblclick", (e) => {
		console.log("tile double clicked");
		let tileRotation = parseInt( e.target.style.transform.match(/\d+/) );
		console.log(`tileRotation : ${tileRotation}`);
		tileRotation = (tileRotation + 90) % 360;
		console.log(`tileRotation : ${tileRotation}`);
		e.target.style.transform = "rotate("+tileRotation+"deg)";
	});
}
// retourne une liste de transformations de tuiles (voir hashSolution())
function getSolution(puzzleTilesElements)
{
	let res = [];
	for( tileElement of puzzleTilesElements ){
		let parentCell = tileElement.parentElement;
		if( !parentCell || !parentCell.classList.contains("puzzle-cell") )
			continue;

		let tileId = parseInt( tileElement.id.split("-")[2] );
		let cellIdData = parentCell.id.split("-");
		let tileRow = parseInt( cellIdData[2] );
		let tileCol = parseInt( cellIdData[3] );
		let tileRot = parseInt( tileElement.firstElementChild.firstElementChild.style.transform.match(/\d+/) );
		// let tileRot = 0;
		res.push( {"id": tileId, "row": tileRow, "col": tileCol, "rotDeg": tileRot} );
	}
	res.sort((a, b) => {
        if (a.row !== b.row) return a.row - b.row;
        return a.col - b.col;
    });
	console.log(`res : ${res}`);
	return res;
}

// DOIT ETRE FONCTIONNELLEMENT IDENTIQUE A LA FONCTION HASH DU SERVEUR
function hashSolution(solution, size){
	const offset = 13;
	let res = "";
	let char = 0;
	for( const tileConfig of solution ){
		char = tileConfig.row * size + tileConfig.col + tileConfig.rotDeg;
		res += String.fromCharCode(char + offset);
	}
	return res;
}