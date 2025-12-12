from services.database_manager import DatabaseManager

class ITTicket:
    def __init__(self, ticket_id: int, display_id: str, subject: str, priority: str, status: str, category: str, description: str, created_date: str, resolved_date: str, assigned_to: str):
        self.__id = ticket_id
        self.__display_id = display_id
        self.__subject = subject
        self.__priority = priority
        self.__status = status
        self.__category = category
        self.__description = description
        self.__created_date = created_date
        self.__resolved_date = resolved_date
        self.__assigned_to = assigned_to

    def get_id(self) -> int:
        return self.__id
    
    def get_display_id(self) -> str:
        return self.__display_id
    
    def get_subject(self) -> str:
        return self.__subject

    def get_priority(self) -> str:
        return self.__priority
    
    def get_status(self) -> str:
        return self.__status

    def get_category(self) -> str:
        return self.__category

    def get_description(self) -> str:
        return self.__description

    def get_created_date(self) -> str:
        return self.__created_date

    def get_resolved_date(self) -> str:
        return self.__resolved_date
    
    def get_assigned_to(self) -> str:
        return self.__assigned_to

    def to_dict(self):
        return {
            "Internal ID": self.__id,
            "Ticket ID": self.__display_id,
            "Subject": self.__subject,
            "Priority": self.__priority,
            "Status": self.__status,
            "Category": self.__category,
            "Description": self.__description,
            "Created Date": self.__created_date,
            "Resolved Date": self.__resolved_date,
            "Assigned To": self.__assigned_to
        }

class TicketRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert_ticket(self, ticket_id_str, priority, status, category, subject, description, created_date):
        query = """
            INSERT INTO it_tickets 
            (ticket_id, priority, status, category, subject, description, created_date, assigned_to) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (ticket_id_str, priority, status, category, subject, description, created_date, "Unassigned"))

    def get_all_tickets(self):
        query = "SELECT * FROM it_tickets ORDER BY id DESC"
        df = self.db.fetch_data(query)
        
        tickets = []
        if not df.empty:
            for _, row in df.iterrows():
                tickets.append(ITTicket(
                    ticket_id=row['id'], 
                    display_id=row['ticket_id'],
                    subject=row['subject'], 
                    priority=row['priority'], 
                    status=row['status'],
                    category=row['category'],
                    description=row['description'],
                    created_date=row['created_date'],
                    resolved_date=row['resolved_date'],
                    assigned_to=row['assigned_to'] if row['assigned_to'] else "Unassigned"
                ))
        return tickets

    def update_ticket_status(self, id, status):
        self.db.execute_query("UPDATE it_tickets SET status = ? WHERE id = ?", (status, id))

    def delete_ticket(self, id):
        self.db.execute_query("DELETE FROM it_tickets WHERE id = ?", (id,))