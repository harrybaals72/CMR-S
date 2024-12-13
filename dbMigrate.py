import sqlite3
import os

def add_folder_column(cursor, db_path):
	cursor.execute("PRAGMA table_info(posts)")
	columns = [column[1] for column in cursor.fetchall()]

	if 'folder' not in columns:
		print(f"Column 'folder' does not exist in {db_path}")
		# Create a new table with the desired schema
		cursor.execute('''
			CREATE TABLE posts_new (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				post_id INTEGER,
				date TEXT,
				text TEXT,
				filename TEXT,
				folder TEXT,
				path TEXT,
				mediaType INTEGER,
				downloaded INTEGER DEFAULT 0
			)
		''')

		print(f"New table 'posts_new' created")
		# Copy data from the old table to the new table
		cursor.execute('''
			INSERT INTO posts_new (id, post_id, date, text, filename, path, mediaType, downloaded)
			SELECT id, post_id, date, text, filename, path, mediaType, downloaded
			FROM posts
		''')

		# Drop the old table
		print(f"Dropping old table 'posts'")
		cursor.execute("DROP TABLE posts")

		# Rename the new table to the original table name
		print(f"Renaming new table to 'posts'")
		cursor.execute("ALTER TABLE posts_new RENAME TO posts")

def add_serverPath_column(cursor, db_path):
	cursor.execute("PRAGMA table_info(posts)")
	columns = [column[1] for column in cursor.fetchall()]

	if 'serverPath' not in columns:
		print(f"Column 'serverPath' does not exist in {db_path}")
		# Create a new table with the desired schema
		cursor.execute('''
			CREATE TABLE posts_new (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				post_id INTEGER,
				date TEXT,
				text TEXT,
				filename TEXT,
				folder TEXT,
				serverPath TEXT,
				path TEXT,
				mediaType INTEGER,
				downloaded INTEGER DEFAULT 0
			)
		''')

		print(f"New table 'posts_new' created with 'serverPath' column")
		# Copy data from the old table to the new table
		cursor.execute('''
			INSERT INTO posts_new (id, post_id, date, text, filename, folder, path, mediaType, downloaded)
			SELECT id, post_id, date, text, filename, folder, path, mediaType, downloaded
			FROM posts
		''')

		# Drop the old table
		print(f"Dropping old table 'posts'")
		cursor.execute("DROP TABLE posts")

		# Rename the new table to the original table name
		print(f"Renaming new table to 'posts'")
		cursor.execute("ALTER TABLE posts_new RENAME TO posts")


def process_db(db_path):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# Check if the 'posts' table exists
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
	table_exists = cursor.fetchone()
	
	if table_exists:
		add_folder_column(cursor, db_path)
		print("")
		add_serverPath_column(cursor, db_path)
		conn.commit()
	else:
		print(f"Table 'posts' does not exist in {db_path}")
		
	print("-------------------------------")
	print("")
	conn.close()


def main():
	folder_path = './'
	for filename in os.listdir(folder_path):
		if filename.endswith('.db'):
			db_path = os.path.join(folder_path, filename)
			
			# print(f"Processing {db_path}")
			process_db(db_path)

if __name__ == "__main__":
	main()