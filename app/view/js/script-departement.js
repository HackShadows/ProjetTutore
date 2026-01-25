
function selectionDepartement(number) {
	console.log(`Le département cliqué est le ${number}`);
	const params = {
		number: String(number),
	};
	const options = {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(params),
	};
	fetch('/selectionDepartement', options)
		.then(response => response.json())
		.then(data => {
			if (data.redirect_url) {
				window.location.href = data.redirect_url;
			}
		})
		.catch(error => console.error("Erreur:", error));
}