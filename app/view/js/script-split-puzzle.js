function splitImage(url, puzzlesize, tilesize) {
	return new Promise((resolve, reject) => {
		const tiles = [];
		const img = new Image();
		img.crossOrigin = "Anonymous";
		img.onload = () => {
			const sourceStepX = img.width / puzzlesize;
			const sourceStepY = img.height / puzzlesize;
			console.log(`taille de sourceStep : ${sourceStepY}`);
			for (let row = 0; row < puzzlesize; row++) {
				for (let col = 0; col < puzzlesize; col++) {
					const canvas = document.createElement("canvas");
					canvas.width = tilesize;
					canvas.height = tilesize;
					const context = canvas.getContext("2d");
					console.log(`taille du canva : ${tilesize}`)
					context.drawImage(
						img,
						col * sourceStepX, row * sourceStepY, // Source X, Y (début de la coupe)
						sourceStepX, sourceStepY,             // Source W, H (taille de la coupe)
						0, 0,                                 // Destination X, Y
						tilesize, tilesize                  // Destination W, H (redimensionnement force)
					);
					tiles.push({
						id: row * puzzlesize + col,
						img: canvas.toDataURL(),
					});
				}
			}
			resolve(tiles);
		};
		img.onerror = (err) => {
			console.error("Erreur chargement image", err);
			reject(err);
		};
		img.src = url;
	});
}

async function demarrerJeu() {
	const url = document.getElementById('imageurl').value;
	const puzzlesize = document.getElementById('imagesize').value;
	// const tilesize = document.getElementById('cellsize').value;
	const tilesize = 300;

	if (url) {
		try {
			const tiles = await splitImage(url, puzzlesize, tilesize);
			console.log("Pièces générées :", tiles);
			for (let i = 0; i < puzzlesize * puzzlesize; i++) {
				document.getElementById("tile" + i).src = tiles[i]['img'];
			}
			console.log("done")
		} catch (error) {
			console.error("Problème de génération du puzzle", error);
		}
	}
}

demarrerJeu()