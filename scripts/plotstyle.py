from matplotlib import pyplot as plt
import fire
import os

FIGURE_PATH = "../figures"

def defaultStyle(fs=14):
    plt.rc("font", family="Arial")
    plt.rc("text", usetex=False)
    plt.rc("xtick", labelsize=fs)
    plt.rc("ytick", labelsize=fs)
    plt.rc("axes", labelsize=fs)
    plt.rc("mathtext", fontset="custom", rm="Arial")


def save_fig(fig_id, tight_layout=True, fmt="pdf"):
    path = os.path.join(FIGURE_PATH, fig_id + ".%s"%fmt)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fmt, transparent=True)


if __name__ == "__main__":
    fire.Fire()
