import abc
import xarray as xr
from tsdat.config import Config
from tsdat.standards import Standards
from tsdat.io.storage import DatastreamStorage


class Pipeline(abc.ABC):

    def __init__(self, config: Config, storage: DatastreamStorage) -> None:
        self.storage = storage
        self.config = config
        pass

    @abc.abstractmethod
    def run(self, filepath: str):
        return

    def standardize(self, dataset: xr.Dataset) -> xr.Dataset:
        """-------------------------------------------------------------------
        Standardizes the dataset by applying variable name and units 
        conversions as defined in the config. Returns the standardized 
        dataset.

        Args:
            dataset (xr.Dataset):   The raw xarray dataset.

        Returns:
            xr.Dataset: The standardized dataset.
        -------------------------------------------------------------------"""
        definition = self.config.dataset_definition

        for coordinate in definition.coords.values():
            definition.extract_data(coordinate, dataset)
        
        for variable in definition.vars.values():
            definition.extract_data(variable, dataset)

        standardized_dataset = xr.Dataset.from_dict(definition.to_dict())
        self.validate_dataset(standardized_dataset)
        return standardized_dataset
    
    def validate_dataset(self, dataset: xr.Dataset):
        """-------------------------------------------------------------------
        Confirms that the dataset conforms with MHKiT-Cloud data standards. 
        Raises an error if the dataset is improperly formatted. This method 
        should be overridden if different standards or validation checks 
        should be applied.

        Args:
            dataset (xr.Dataset): The dataset to validate.
        -------------------------------------------------------------------"""
        Standards.validate(dataset)
 