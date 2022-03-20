import numpy as np
from skimage.segmentation import find_boundaries
import skimage.io
import matplotlib.pyplot as plt
from skimage.measure import regionprops
import pandas as pd
import os
import fire


def show_seg(seg_file, img_file=None, ax=None, region=None, adjust=5, chan=0, boundary_intensity=1):
    # Input file is the segmentation output of *Cellpose*
    # No return. Show segmentation image
    try:
        seg_data = np.load(seg_file, allow_pickle=True).item()
        outlines = seg_data["outlines"]
    except:
        outlines = find_boundaries(np.load(seg_data))
    if img_file is None:
        img = seg_data["img"]
    else:
        img = skimage.io.imread(img_file)
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(10, 10))
    if len(img.shape) == 3:
        if img.shape[2] == 3:
            img = img[:, :, chan]
        else:
            img = img[chan, :, :]
    if region is None:
        region = [0, img.shape[0], 0, img.shape[1]]
    im_cut = img[region[0] : region[1], region[2] : region[3]]
    outline_cut = outlines[region[0] : region[1], region[2] : region[3]]
    im_cut = im_cut / np.max(im_cut) * adjust
    im_rgb = np.zeros((im_cut.shape[0], im_cut.shape[1], 3))
    im_rgb[:, :, chan] = im_cut
    im_rgb[outline_cut > 0] = boundary_intensity
    ax.imshow(im_rgb)
    ax.axis("off")


def show_seg_composite(
    seg_file_1, seg_file_2, ax=None, region=None, adjust_1=2, adjust_2=5
):
    # Input file is the segmentation output of *Cellpose*
    # No return. Show segmentation image
    im_cut_group = []
    outline_cut_group = []
    for seg_file, adjust in zip([seg_file_1, seg_file_2], [adjust_1, adjust_2]):
        seg_data = np.load(seg_file, allow_pickle=True).item()
        outlines, img = seg_data["outlines"], seg_data["img"]
        if region is None:
            region = [0, seg_data["img"].shape[0], 0, seg_data["img"].shape[1]]
        print("Number of cells: %d" % np.max(outlines))
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(10, 10))
        im_cut = img[region[0] : region[1], region[2] : region[3]]
        outline_cut = outlines[region[0] : region[1], region[2] : region[3]]
        im_cut = im_cut / np.max(im_cut) * adjust
        im_cut_group.append(im_cut)
        outline_cut_group.append(outline_cut)
    im_rgb = np.zeros((im_cut.shape[0], im_cut.shape[1], 3))
    im_rgb[:, :, 0] = im_cut_group[0]
    im_rgb[:, :, 1] = im_cut_group[1]
    im_rgb[:, :, 0][outline_cut_group[0] > 0] = 0.7
    im_rgb[:, :, 1][outline_cut_group[1] > 0] = 0.7
    ax.imshow(im_rgb)
    ax.axis("off")


def mean_intensity_of_max_n_pixels(intensity_im, n=16):
    intensity_arr = intensity_im.flatten()
    if len(intensity_arr) >= n:
        return np.mean(intensity_arr[np.argsort(intensity_arr)[-n:]])
    else:
        return np.mean(intensity_arr)


def extract_fl_loc(seg_file, img_file, chan=0):
    try:
        seg_data = np.load(seg_file, allow_pickle=True).item()
        masks = seg_data["masks"]
    except ValueError:
        masks = np.load(seg_file)
    img = skimage.io.imread(img_file)
    if len(img.shape) > 1:
        img = img[:, :, chan]
    return regionprops(masks, intensity_image=img)


def extract_fl_loc_table(seg_path):
    imageinfo_group = []
    for chan in ["red", "green"]:
        seg_file = os.path.join(seg_path, "%s.npy" % chan)
        red_img = os.path.join(raw_img_path(group), "red.tif")
        green_img = os.path.join(raw_img_path(group), "green.tif")
        props_red = extract_fl_loc(seg_file, red_img)
        props_green = extract_fl_loc(seg_file, green_img)
        imageinfo_data = np.array(
            [
                [
                    mean_intensity_of_max_n_pixels(props_red[i].intensity_image),
                    mean_intensity_of_max_n_pixels(props_green[i].intensity_image),
                    props_red[i].max_intensity,
                    props_green[i].max_intensity,
                    props_red[i].centroid,
                    props_red[i].perimeter,
                    props_red[i].area,
                    props_red[i].eccentricity,
                    i + 1,
                ]
                for i in range(len(props_red))
            ],
            dtype=object,
        )
        imageinfo_df = pd.DataFrame(
            imageinfo_data,
            columns=[
                "red_fl",
                "green_fl",
                "max_red_fl",
                "max_green_fl",
                "loc",
                "perimeter",
                "area",
                "eccentricity",
                "label",
            ],
        )
        imageinfo_df["chan"] = chan
        imageinfo_group.append(imageinfo_df)
    imageinfo_df = pd.concat(imageinfo_group).reset_index(drop=True)
    return imageinfo_df


if __name__ == "__main__":
    fire.Fire()
