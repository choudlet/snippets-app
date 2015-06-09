import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='christopherhoudlette' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    try:
    	command ="insert into snippets values (%s, %s);"
    	cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
    	connection.rollback()
    	command = "update snippets set message=%s where keyword=%s"
    	cursor.execute(command, (snippet, name))
    connection.commit()
    logging.info("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet - return error
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    cursor.execute("select message from snippets where keyword=%s", (name,))
    message = cursor.fetchone()
    connection.commit()  
    if not message:
    	logging.error("Tried to get {!r} snippet but does not exist!".format(name))
    	print "That doesn't exist you fool!"
    else:
    	cursor.fetchone()  	
   	logging.info("Snippet fetched successfully")
    	return message[0]
def catalog():
	"""
	List previously created snippets
	"""
	logging.info("Retrieving catalog")
	cursor = connection.cursor()
	cursor.execute("select keyword from snippets order by keyword asc")
	rows = cursor.fetchall()
	for row in rows:
		print row
	
def main():
	"""Main Function"""
	logging.info("Constructing Parser")
	parser = argparse.ArgumentParser(description="store and retrieve snippets of text")
	
	subparsers = parser.add_subparsers(dest="command", help="Available commands")
	
	#subparser for the put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help="Store a snippet")
	put_parser.add_argument("name", help="The name of the snippet")
	put_parser.add_argument("snippet", help="The snippet text")
	
	#subparser for the get command
	get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
	get_parser.add_argument("name", help="name of the snippet you want")
	
	#subparser for the catalog command
	catalog_parser = subparsers.add_parser("catalog", help="List catalog of prev. stored snippets")
	
	arguments = parser.parse_args(sys.argv[1:])
	#Convert parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	command = arguments.pop("command")
	
	if command == "put":
		name, snippet = put(**arguments)
		print ("Stored {!r} as {!r}".format(snippet, name))
	elif command == "get":
		name = get(**arguments)
		print ("Retrieved snippet {!r}".format(name))
	elif command == "catalog":
		catalog()
		print "These are all the current keywords in the database"

if __name__ == "__main__":
	main()