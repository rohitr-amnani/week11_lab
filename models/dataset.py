from services.database_manager import DatabaseManager

class Dataset:
    def __init__(self, dataset_id: int, name: str, size_mb: float, rows: int, source: str, category: str, last_updated: str):
        self.__id = dataset_id
        self.__name = name
        self.__size_mb = size_mb
        self.__rows = rows
        self.__source = source
        self.__category = category
        self.__last_updated = last_updated

    def get_id(self) -> int:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name

    def get_size_mb(self) -> float:
        return self.__size_mb

    def get_row_count(self) -> int:
        return self.__rows

    def get_source(self) -> str:
        return self.__source

    def get_category(self) -> str:
        return self.__category

    def get_last_updated(self) -> str:
        return self.__last_updated

    def to_dict(self):
        return {
            "ID": self.__id,
            "Dataset Name": self.__name,
            "Category": self.__category,
            "Source": self.__source,
            "Last Updated": self.__last_updated,
            "Record Count": self.__rows,
            "Size (MB)": self.__size_mb
        }

class DatasetRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert_dataset(self, name, category, source, date, count, size_mb):
        query = """
            INSERT INTO datasets_metadata 
            (dataset_name, category, source, last_updated, record_count, file_size_mb) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (name, category, source, date, count, size_mb))

    def get_all_datasets(self):
        query = "SELECT * FROM datasets_metadata ORDER BY id DESC"
        df = self.db.fetch_data(query)
        
        datasets = []
        if not df.empty:
            for _, row in df.iterrows():
                datasets.append(Dataset(
                    dataset_id=row['id'], 
                    name=row['dataset_name'], 
                    size_mb=row['file_size_mb'], 
                    rows=row['record_count'],
                    source=row['source'],
                    category=row['category'],
                    last_updated=row['last_updated']
                ))
        return datasets
        
    def delete_dataset(self, id):
        self.db.execute_query("DELETE FROM datasets_metadata WHERE id = ?", (id,))