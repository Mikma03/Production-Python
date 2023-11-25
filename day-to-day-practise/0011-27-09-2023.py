class Test:
    @staticmethod
    def load_data(json_path: str):
        file_content = dbutils.fs.head(json_path)
        data = json.loads(file_content)
        return data

    def get_spark_schema_from_json(data: str) -> StructType:
        """
        Reads a JSON schema file from DBFS and constructs a Spark StructType schema from it.
        
        :param file_path: Path to the JSON schema file in DBFS.
        :return: Spark StructType schema.
        """
        # Mapping of string type names to actual Spark DataTypes
        type_mapping = {
            "integer": IntegerType(),
            "string": StringType(),
            "double": DoubleType()
            # Add other types as needed
        }
        
        # Read the JSON file from DBFS
        json_content = data
        
        # Construct the Spark schema
        fields = []
        for field_info in json_content["fields"]:
            field_name = field_info["name"]
            field_type = type_mapping.get(field_info["type"], StringType())  # Default to StringType if type is not recognized
            field_nullable = field_info.get("nullable", True)
            field_metadata = field_info.get("metadata", {})
            
            fields.append(StructField(field_name, field_type, nullable=field_nullable, metadata=field_metadata))
        
        return StructType(fields)
