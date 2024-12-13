import sqlite3
import os

def add_serverFileName_column(cursor, db_path):
	# Create a new table with the desired schema
	cursor.execute('''
		CREATE TABLE posts_new (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			post_id INTEGER,
			date TEXT,
			text TEXT,
			serverFileName TEXT,
			localFileName TEXT,
			folder TEXT,
			serverPath TEXT,
			post_url TEXT,
			mediaType INTEGER,
			downloaded INTEGER DEFAULT 0
		)
	''')

	# Copy data from the old table to the new table
	cursor.execute('''
    INSERT INTO posts_new (id, post_id, date, text, localFileName, folder, serverPath, post_url, mediaType, downloaded)
    SELECT id, post_id, date, text, filename, folder, serverPath, path, mediaType, downloaded
    FROM posts
	''')

	# Drop the old table
	cursor.execute('DROP TABLE posts')

	# Rename the new table to the original table name
	cursor.execute('ALTER TABLE posts_new RENAME TO posts')


def process_db(db_path):
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# Check if the 'posts' table exists
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
	table_exists = cursor.fetchone()
	
	if table_exists:
		# add_folder_column(cursor, db_path)
		# print("")
		# add_serverPath_column(cursor, db_path)
		add_serverFileName_column(cursor, db_path)
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