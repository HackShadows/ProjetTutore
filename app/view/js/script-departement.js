
function selectionDepartement(number, name) {
	console.log(`Le département cliqué est le ${number}, ${name}`);
	const params = {
		number: String(number),
		name: name,
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