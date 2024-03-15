from __init__ import CURSOR, CONN

class Department:
    all = {}

    def __init__(self, name, location):
        self.id = None
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        CONN.commit()

    def save(self):
        CURSOR.execute("INSERT INTO departments (name, location) VALUES (?, ?)", (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        cls.all[department.id] = department
        return department

    def update(self):
        if self.id is None:
            raise ValueError("Cannot update department without id.")
        CURSOR.execute("UPDATE departments SET name=?, location=? WHERE id=?", (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        if self.id is None:
            raise ValueError("Cannot delete department without id.")
        CURSOR.execute("DELETE FROM departments WHERE id=?", (self.id,))
        CONN.commit()
        del self.all[self.id]

    @classmethod
    def instance_from_db(cls, row):
        if row:
            return cls(row[1], row[2])

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM departments")
        rows = CURSOR.fetchall()
        departments = []
        for row in rows:
            departments.append(cls.instance_from_db(row))
        return departments

    @classmethod
    def find_by_id(cls, department_id):
        return cls.all.get(department_id)

    @classmethod
    def find_by_name(cls, name):
        for department in cls.all.values():
            if department.name == name:
                return department
