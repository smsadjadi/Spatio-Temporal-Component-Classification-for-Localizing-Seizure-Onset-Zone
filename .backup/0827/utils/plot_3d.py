import matplotlib.pyplot as plt

def plot_3d(data):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(data[:, :, data.shape[2] // 2], cmap="gray")
    axes[0].set_title("Axial Slice")
    axes[0].axis("off")
    axes[1].imshow(data[:, data.shape[1] // 2, :], cmap="gray")
    axes[1].set_title("Coronal Slice")
    axes[1].axis("off")
    axes[2].imshow(data[data.shape[0] // 2, :, :], cmap="gray")
    axes[2].set_title("Sagittal Slice")
    axes[2].axis("off")
    plt.show()