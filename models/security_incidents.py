from services.database_manager import DatabaseManager

#create SecurityIncident class
class SecurityIncident:
    def __init__(self, incident_id: int, date: str, incident_type: str, severity: str, status: str, description: str, reported_by: str):
        self.__id = incident_id
        self.__date = date
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__reported_by = reported_by

    def get_id(self) -> int:
        return self.__id

    def get_date(self) -> str:
        return self.__date

    def get_type(self) -> str:
        return self.__incident_type

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description
    
    def get_reported_by(self) -> str:
        return self.__reported_by

    #create dictionary representation to facilitate DataFrame conversion
    def to_dict(self):
        return {
            "ID": self.__id,
            "Date": self.__date,
            "Incident Type": self.__incident_type,
            "Severity": self.__severity,
            "Status": self.__status,
            "Description": self.__description,
            "Reported By": self.__reported_by
        }

class Incident:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    #insert incident method
    def insert_incident(self, date, incident_type, severity, status, description, reported_by):
        query = """
            INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (date, incident_type, severity, status, description, reported_by))

    #read all incidents method
    def get_all_incidents(self):
        query = "SELECT * FROM cyber_incidents ORDER BY id DESC"
        df = self.db.fetch_data(query)
        
        incidents = []
        if not df.empty:
            for _, row in df.iterrows():
                incidents.append(SecurityIncident(
                    incident_id=row['id'],
                    date=row['date'],
                    incident_type=row['incident_type'], 
                    severity=row['severity'], 
                    status=row['status'], 
                    description=row['description'],
                    reported_by=row['reported_by']
                ))
        return incidents
    
    #update incident status method
    def update_incident_status(self, id, status):
        self.db.execute_query("UPDATE cyber_incidents SET status = ? WHERE id = ?", (status, id))

    #delete incident method
    def delete_incident(self, id):
        self.db.execute_query("DELETE FROM cyber_incidents WHERE id = ?", (id,))