from typing import Dict, Any
from tsdat.exceptions import DefinitionError


class PipelineKeys:
    TYPE = 'type'
    INPUT_DATA_LEVEL = 'input_data_level'
    OUTPUT_DATA_LEVEL = 'output_data_level'
    
    LOCATION_ID = 'location_id'
    INSTRUMENT_ID = 'instrument_id'
    QUALIFIER = 'qualifier'
    TEMPORAL = 'temporal'


class PipelineDefinition:

    def __init__(self, dictionary: Dict[str, Any]):
        self.dictionary = dictionary

        # Parse pipeline type and output data level
        valid_types = ["Ingest", "VAP"]
        pipeline_type = dictionary.get(PipelineKeys.TYPE, None)
        if pipeline_type not in valid_types:
            raise DefinitionError(f"Pipeline type must be one of: {valid_types}")
        self.type: str = pipeline_type

        # Parse input data level
        default_input_data_level = {"Ingest": "00", "VAP": "a1"}.get(pipeline_type)
        input_data_level = dictionary.get(PipelineKeys.INPUT_DATA_LEVEL, default_input_data_level)
        self.input_data_level: str = input_data_level

        # Parse output data level
        default_output_data_level = {"Ingest": "a1", "VAP": "b1"}.get(pipeline_type)
        output_data_level = dictionary.get(PipelineKeys.OUTPUT_DATA_LEVEL, default_output_data_level)
        self.output_data_level: str = output_data_level

        # Parse file naming components
        self.location_id = dictionary.get(PipelineKeys.LOCATION_ID)
        self.instrument_id = dictionary.get(PipelineKeys.INSTRUMENT_ID)
        self.qualifier = dictionary.get(PipelineKeys.QUALIFIER, "")
        self.temporal = dictionary.get(PipelineKeys.TEMPORAL, "")
        
        self.check_file_name_components()

        # Parse datastream_name
        base_datastream_name = f"{self.location_id}.{self.instrument_id}"
        if self.qualifier:
            base_datastream_name += f"-{self.qualifier}"
        if self.temporal:
            base_datastream_name += f"-{self.temporal}"
        self.input_datastream_name = f"{base_datastream_name}.{input_data_level}"
        self.output_datastream_name = f"{base_datastream_name}.{output_data_level}"

    def check_file_name_components(self):
        illegal_characters = [".", "-", " "]
        components_to_check = [self.location_id, self.instrument_id, self.qualifier, self.temporal]
        valid = lambda component: sum([bad_char in component for bad_char in illegal_characters]) == 0
        bad_components = [component for component in components_to_check if not valid(component)]
        if bad_components:
            message = f"The following properties contained one or more illegal characters: "
            message += f"{bad_components}\n"
            message += f"Illegal characters include: {illegal_characters}"
            raise DefinitionError(message)
