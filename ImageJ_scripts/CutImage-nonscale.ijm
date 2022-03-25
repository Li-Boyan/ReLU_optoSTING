n = 3;
id = getImageID(); 
title = getTitle();
dotIndex = indexOf(title, "." );
nameWithoutExtension = substring(title, 0, dotIndex);
getLocationAndSize(locX, locY, sizeW, sizeH); 
width = getWidth(); 
height = getHeight(); 
tileWidth = width / n; 
tileHeight = height / n; 
path = getInfo("image.directory");
idx = 1
for (y = 0; y < n; y++) { 
	offsetY = y * height / n; 
	for (x = 0; x < n; x++) { 
		offsetX = x * width / n; 
		selectImage(id); 
		call("ij.gui.ImageWindow.setNextLocation", locX + offsetX, locY + offsetY); 
		titleTitle = title + " [" + x + "," + y + "]"; 
		run("Duplicate...", "title=" + titleTitle + " duplicate");
		makeRectangle(offsetX, offsetY, tileWidth, tileHeight); 
		run("Crop");
		run("Smooth");
		run("Median...", "radius=2");
		saveAs("Tiff", path + nameWithoutExtension + "-" + idx + "-nonscale.tif");
		close();
		idx ++;
	}
}
