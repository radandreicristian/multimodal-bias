from datasets import load_dataset
from torch.utils.data import Dataset
from typing import Optional, Any, Dict

class ImageDataset(Dataset):
    """Class for structuring the dataset."""

    def __init__(self,
                 ids: list[int],
                 text: list[str],
                 url: list[str]):
        """Format dataset.
        
        Args:
            ids: list of the ids of images.
            text: list of the ids of images.
            url: list of the urls of images.
        """
        self.ids = ids
        self.text = text
        self.url = url
    
    def __len__(self) -> int:
        """
        Compute the length of the dataset (number of samples).

        :return: The length of the dataset.
        """
        return len(self.text)
    
    def __getitem__(self, index) -> Dict[str, Any]:
        return {'id' : self.ids[index],
                'text' : self.text[index],
                'url' : self.url[index]}
        
class DataModule:
    """Module for loading dataset"""
    
    def __init__(self):
        """Loads dataset"""
        raw_dataset = dict()
        raw_dataset = load_dataset("parquet", data_files='laion_face_meta\laion_face_part_00000.parquet')
        self.dataset: Optional[Dataset] = ImageDataset(raw_dataset['train']['SAMPLE_ID'], raw_dataset['train']['TEXT'], raw_dataset['train']['URL'])
