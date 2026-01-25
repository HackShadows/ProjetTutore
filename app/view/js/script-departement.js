
function selectionDepartement(number) {
	console.log(`Vous avez cliqué sur le ${number}`);
	const params = {
		number: String(number),
	};
	const options = {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(params),
	};
	fetch('/selectionDepartement', options)
	.then(response => response.json()) // 2. On lit la réponse JSON
    .then(data => {
        // 3. Si le serveur nous donne une URL, on y va !
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => console.error("Erreur:", error));
}