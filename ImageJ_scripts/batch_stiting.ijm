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

function pairwise_stitching(path, m,  n){
	for (i=m; i<=n; i++){
		mergeChannels(path + "/" + "Pos" + i);
		if (i==m)
			rename("merge_1.tif");
		else{
			rename("merge_2.tif");
			run("Pairwise stitching", "first_image=merge_1.tif second_image=merge_2.tif fusion_method=[Average] fused_image=fused check_peaks=50 compute_overlap x=0.0000 y=0.0000 registration_channel_image_1=[Average all channels] registration_channel_image_2=[Average all channels]");
			selectWindow("merge_1.tif");
			close();
			selectWindow("merge_2.tif");
			close();
			selectWindow("fused");
			rename("merge_1.tif");
		}
	}
}

firstidx = 98;
secondidx = 106;
pairwise_stitching("/home/liboyan/Documents/optoSTING/data/20211220/1-20_-light/1-20_-light_2", firstidx, secondidx);
rename("stitched_" + firstidx + "-" + secondidx);