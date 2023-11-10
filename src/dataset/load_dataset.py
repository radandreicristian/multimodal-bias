from datasets import load_dataset
from torch.utils.data import Dataset
from typing import Optional, Any, Dict

class ImageDataset(Dataset):
    def __init__(self,
                 ids,
                 text,
                 url):
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
        
class TrainDataModule():

    def __init__(self):
        raw_dataset = dict()
        raw_dataset = load_dataset("parquet", data_files='laion_face_meta\laion_face_part_00000.parquet')
        self.train_dataset: Optional[Dataset] = ImageDataset(raw_dataset['train']['SAMPLE_ID'], raw_dataset['train']['TEXT'], raw_dataset['train']['URL'])
