function mergeChannels(path){
	all_files = getFileList(path);
	for (i=0; i<all_files.length; i++){
		if (endsWith(all_files[i], ".tif")){
			open(path + "/" + all_files[i]);
			selectWindow(all_files[i]);
			if (indexOf(all_files[i], "mcherry") >=0)
				rename("mCherry.tif");
			else if (indexOf(all_files[i], "FITC") >= 0)
				rename("GFP.tif");
			else if (indexOf(all_files[i], "BF") >= 0)
				rename("BF.tif");
		}
	}
	run("Merge Channels...", "c1=mCherry.tif c2=GFP.tif c4=BF.tif create");
}

i = 97;
mergeChannels("/home/liboyan/Documents/optoSTING/data/20211220/1-20_-light/1-20_-light_2" + "/" + "Pos" + i);
rename(i)