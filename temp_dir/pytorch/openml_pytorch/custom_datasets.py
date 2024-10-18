"""
This module contains custom dataset classes for handling image and tabular data from OpenML in PyTorch. To add support for new data types, new classes can be added to this module.
"""
import os
from typing import Any
import pandas as pd
from sklearn import preprocessing
import torch
from torchvision.io import read_image
from torch.utils.data import Dataset
# from torchvision.transforms import Compose, Resize, ToPILImage, ToTensor, Lambda
import torchvision.transforms as T

class OpenMLImageDataset(Dataset):
    """
        Class representing an image dataset from OpenML for use in PyTorch.

        Methods:

            __init__(self, X, y, image_size, image_dir, transform_x=None, transform_y=None)
                Initializes the dataset with given data, image size, directory, and optional transformations.

            __getitem__(self, idx)
                Retrieves an image and its corresponding label (if available) from the dataset at the specified index. Applies transformations if provided.

            __len__(self)
                Returns the total number of images in the dataset.
    """
    def __init__(self, X, y, image_size, image_dir, transform_x = None, transform_y = None):
        self.X = X
        self.y = y
        self.image_size = image_size
        self.image_dir = image_dir
        self.transform_x = transform_x
        self.transform_y = transform_y

    def __getitem__(self, idx):
        img_name = str(os.path.join(self.image_dir, self.X.iloc[idx, 0]))
        image = read_image(img_name)
        image = image.float()
        image = T.Resize((self.image_size, self.image_size))(image)
        if self.transform_x is not None:
            image = self.transform_x(image)
        if self.y is not None:
            label = self.y.iloc[idx]
            if label is not None:
                if self.transform_y is not None:
                    label = self.transform_y(label)
                return image, label
        else:
            return image
    
    def __len__(self):
        return len(self.X)


class OpenMLTabularDataset(Dataset):
    """
    OpenMLTabularDataset

    A custom dataset class to handle tabular data from OpenML (or any similar tabular dataset).
    It encodes categorical features and the target column using LabelEncoder from sklearn.

    Methods:
        __init__(X, y) : Initializes the dataset with the data and the target column.
                         Encodes the categorical features and target if provided.

        __getitem__(idx): Retrieves the input data and target value at the specified index.
                          Converts the data to tensors and returns them.

        __len__(): Returns the length of the dataset.
    """
    def __init__(self, X, y):
        self.data = X
        # self.target_col_name = target_col
        for col in self.data.select_dtypes(include=['object', 'category']):
            # convert to float
            self.data[col] = self.data[col].astype('category').cat.codes
        self.label_mapping = None

        # self.label_mapping = preprocessing.LabelEncoder()
        # try:
        #     self.data = self.data.apply(self.label_mapping.fit_transform)
        # except ValueError:
        #     pass

        # try:
        #     self.y = self.label_mapping.fit_transform(y)
        # except ValueError:
        #     self.y = None
        self.y = y

    def __getitem__(self, idx):
        # x is the input data, y is the target value from the target column
        x = self.data.iloc[idx, :]
        x = torch.tensor(x.values.astype('float32'))
        if self.y is not None:
            y = self.y[idx]
            y = torch.tensor(y)
            return x, y
        else:
            return x
            

    def __len__(self):
        return len(self.data)
