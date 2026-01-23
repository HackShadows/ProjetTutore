const tileContainer = document.getElementById("tile-container");
let draggedItem = null;

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
		if( targetItem.classList.contains("puzzle-cell"))
		{
			targetItem.insertBefore(draggedItem.parentElement.parentElement, targetItem.firstElementChild);
		}
		else if( targetItem.parentElement.parentElement.classList.contains("puzzle-tile") ) {
			const draggedIndex = [...tileContainer.children].indexOf(draggedItem.parentElement.parentElement);
			const targetIndex = [...tileContainer.children].indexOf(targetItem.parentElement.parentElement);
			if (draggedIndex < targetIndex) {
				tileContainer.insertBefore(draggedItem.parentElement.parentElement, targetItem.parentElement.parentElement.nextSibling);
			}
			else {
				tileContainer.insertBefore(draggedItem.parentElement.parentElement, targetItem.parentElement.parentElement);
			}
		}
		else {
			tileContainer.insertBefore(draggedItem.parentElement.parentElement, tileContainer.children[1]);
		}
	}
});
