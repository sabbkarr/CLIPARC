import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import re
from sklearn.metrics.pairwise import cosine_similarity

!git clone https://github.com/fchollet/ARC-AGI.git
evaluation_challenges_path = '/content/ARC-AGI/data/evaluation/'
evaluation_challenges_path =         '/ARC-AGI/data/evaluation/'

cmap = mcolors.ListedColormap(["#000000","#808080", "#ADD8E6", "#0000FF", "#008000", "#FFFF00", "#FFA500", "#FF0000", "#DC143C", "#FFC0CB"])
def process_json_file(file_path):
    with open(file_path) as fp:
        data = json.load(fp)
        print("Training examples:", len(data['train']))

        for i in range(len(data['train'])):
            input_grid = np.array(data['train'][i]['input'])
            output_grid = np.array(data['train'][i]['output'])
            fig, axes = plt.subplots(1, 2, figsize=(input_grid.shape[1] / 6 + output_grid.shape[1] / 6, max(input_grid.shape[0]/2, output_grid.shape[0]) / 2))

            axes[0].imshow(input_grid, cmap=cmap, interpolation='nearest')
            axes[0].set_title("Input")
            axes[0].axis('off')

            axes[1].imshow(output_grid, cmap=cmap, interpolation='nearest')
            axes[1].set_title("Output")
            axes[1].axis('off')
            plt.show()

        print("Test Input:", len(data['test']))
        test_input_grid = np.array(data['test'][0]['input'])
        plt.figure(figsize=(test_input_grid.shape[1] / 8, test_input_grid.shape[0] / 8))  # Proportional size based on grid dimensions
        plt.imshow(test_input_grid, cmap = cmap, interpolation='nearest')
        plt.axis('off')
        plt.show()

