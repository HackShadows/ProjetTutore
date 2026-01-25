const tileContainer = document.getElementById("tile-container");
let draggedItem = null;

const boardWidth = parseInt( document.getElementById("board-width").innerText );
const boardHeight = parseInt( document.getElementById("board-height").innerText );
const puzzleSolutionHash = parseInt( document.getElementById("solution-hash").innerText);

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
			if( solution.length == boardWidth * boardHeight && hashSolution(solution) == puzzleSolutionHash ) {
				console.log("le puzzle ets fini");
				puzzleSolved = true;
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
for( const containerChild of tileContainer.children){
	if( containerChild.classList.contains("puzzle-tile") ){
		puzzleTiles.push(containerChild);
	}
}

for( puzzleTile of puzzleTiles )
{
	puzzleTile.addEventListener("dblclick", (e) => {
		console.log("tile double clicked");
		let tileRotation = parseInt( e.target.style.transform.match(/\d+/) );
		tileRotation = (tileRotation + 90) % 360;
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

		res.push( {"id": tileId, "row": tileRow, "col": tileCol, "rotDeg": tileRot} );
	}
}

// prend une solution de la forme [{"id": 0, "row": a, "col": b, "rotDeg": c}, ...] et retourne (((a*37 + b)*37 + c)*37 + ...)
// DOIT ETRE FONCTIONNELLEMENT IDENTIQUE A LA FONCTION HASH DU SERVEUR
function hashSolution(solution){
	let res = 0;
	for( const tileConfig of solution ){
		res += tileConfig.row;
		res *= 37;
		res += tileConfig.col;
		res *= 37;
		res += tileConfig.rotDeg;
		res *= 37;
	}
	return res;
}