function splitImage(url, puzzlesize, tilesize) {
    const img = new Image();
    img.src = url;
    let tiles_url = [];
    height = tilesize;
    width = tilesize;
    for(var x = 0; x < puzzlesize; ++x) {
        for(var y = 0; y < puzzlesize; ++y) {
            var canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            var context = canvas.getContext('2d');
            context.drawImage(img, x * width, y * height, width, height, 0, 0, canvas.width, canvas.height);
            tiles_url.push(canvas.toDataURL());
        }
    }
    return tiles_url;
}

url = document.getElementById('imageurl').value;
puzzlesize = document.getElementById('imagesize').value;
tilesize = document.getElementById('cellsize').value;
tiles = splitImage(url,puzzlesize,cellsize);
for (let i = 0 ; i < size*size ; i++) {
    document.getElementById("tile"+i).src = tiles [i];
}
console.log("done");