import matplotlib.pyplot as plt
import matplotlib as mpl

cmaps = [
    "nipy_spectral",
    "gist_ncar",
    "gist_rainbow",
    "turbo",
    "jet",
    "rainbow",
    "brg",
    "hsv",
    "prism",
]

fig, axes = plt.subplots(len(cmaps), 1, figsize=(6, 5), constrained_layout=True)

norm = mpl.colors.Normalize(vmin=-0.3, vmax=0.0)

for ax, cmap_name in zip(axes, cmaps):
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap_name)
    sm.set_array([])

    cbar = fig.colorbar(sm, cax=ax, orientation="horizontal")
    cbar.set_label(cmap_name)

plt.show()