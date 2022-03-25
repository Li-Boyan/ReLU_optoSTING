function reMergeChannels(path, name){
	open(path + "/" + name + "Pos" + i + ".ome.tif");
	rename("new_image.tif");
	run("Split Channels");
	selectWindow("C3-new_image.tif");
	run("Merge Channels...", "c1=C3-new_image.tif c2=C2-new_image.tif c4=C1-new_image.tif create");
}


function pairwise_stitching(path, name, m,  n){
	for (i=m; i<=n; i++){
		reMergeChannels(path, name);
		if (i==m)
			rename("merge_1.tif");
		else{
			rename("merge_2.tif");
			run("Pairwise stitching", "first_image=merge_1.tif second_image=merge_2.tif fusion_method=[Linear Blending] fused_image=fused check_peaks=50 compute_overlap x=0.0000 y=0.0000 registration_channel_image_1=[Average all channels] registration_channel_image_2=[Average all channels]");
			selectWindow("merge_1.tif");
			close();
			selectWindow("merge_2.tif");
			close();
			selectWindow("fused");
			rename("merge_1.tif");
		}
	}
}

firstidx = 71;
secondidx = 81;
pairwise_stitching("/media/liboyan/BOYAN-HD/20220103-1321+PPF98sc8-PPF75/-LIGHT/0h light_1/", "ppf98-sc2_3h light_1_MMStack_", firstidx, secondidx);
rename("stitched_" + firstidx + "-" + secondidx);