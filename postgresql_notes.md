# 🐘 PostgreSQL & Relational Database Learning Notes

## 🛠️ Terminal & Meta-Commands (`psql`)

### `\l`
- to see what databases are available

### `\c database_name`
- to add info to your db, you'll need to connect

### `\d`
- to display tables
- a db is made of tables that holds data

### `\d table_name`
- to view more details about a table

---

## 🗄️ Database Operations

### `CREATE DATABASE database_name;`
- the capitalised words are keywords telling PostgreSQL what to do
- the name of the db is the lowercase word
- all commands need a semi-colon at the end

### `ALTER DATABASE database_name RENAME TO new_database_name;`
- to rename a database

### `DROP DATABASE database_name;`
- to drop a database

---

## 📐 Data Types & Constraints

### `VARCHAR(n)`
- VARCHAR is a short string of characters
- (n) gives it a maximum length

### `SERIAL`
- make a column an INT with a NOT NULL constraint
- automatically increment the integer when a new row is added

### `NUMERIC(x, y)`
- decimal
- has up to x digits
- y of it has to be the right of the decimal (decimal places)

### `DATE`
- need a string with the format 'YYYY-MM-DD'

### Constraints & Relationships
- **Primary Key (PK)**: A column that uniquely identifies each row in the table.
- **Foreign Key (FK)**: Relates rows from a table to another table (`REFERENCES referenced_table_name(referenced_column_name)`).
- **UNIQUE**: Enforce one-to-one relationship between tables (add UNIQUE constraint to FK column).
- **NOT NULL**: Ensures a column cannot be left empty.

---

## 📋 Table & Column Schema Operations (DDL)

### `CREATE TABLE table_name();`
- parenthesis are needed here
- create the table in the db you're connected to
- the new table should have a meta data about it

### `ALTER TABLE table_name ADD COLUMN column_name DATATYPE;`
- to add columns to describe the data in them
- add a constraint by putting it right after the data type (without comma)

### `ALTER TABLE table_name ADD COLUMN column_name DATATYPE REFERENCES referenced_table_name(referenced_column_name);`
- to add a foreign key column
- FK relate rows from a table to another table

### `ALTER TABLE table_name DROP COLUMN column_name;`
- remove column

### `ALTER TABLE table_name RENAME COLUMN column_name TO new_name;`
- to rename a column

### `ALTER TABLE table_name ADD PRIMARY KEY (column_name);`
- to add primary key
- PK is a column that uniquely identifies each row in the table

### `ALTER TABLE table_name ADD UNIQUE(column_name);`
- enforce one-to-one relationship between tables
- add UNIQUE constraint to FK column

### `ALTER TABLE table_name ALTER COLUMN column_name SET NOT NULL;`
- adding NOT NULL constraint to FK column

### `ALTER TABLE table_name DROP CONSTRAINT constraint_name;`
- to drop a constraint
- default primary key constraint name format: `table_name_pkey`

### `DROP TABLE table_name;`
- to drop a table from db

---

## 📝 Data Row Operations & Queries (DML)

### `INSERT INTO table_name(column_1, column_2) VALUES(value1, value2);`
- to add rows which are the actual data in the table

### `SELECT columns FROM table_name;`
- view data in a table
- use comma to separate multiple columns

### `SELECT * FROM table_name;`
- to view all the columns

### `SELECT columns FROM table_name WHERE condition;`
- to view only specific rows matching a condition

### `SELECT columns FROM table_name ORDER BY column_name;`
- to order by
- or replace columns with * to select all

### `UPDATE table_name SET column_name=new_value WHERE condition;`
- to change a value in a row

### `DELETE FROM table_name WHERE condition;`
- delete a record (row)