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
    command ="insert into snippets values (%s, %s);"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.info("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet - return FIXME error
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword='coffee';"
    print name
    cursor.execute("select message from snippets where keyword=%s", (name,))
    message = cursor.fetchone()
    cursor.fetchone()
    connection.commit()
    logging.info("Snippet fetched successfully")
    print message
    return message
    
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
	
	arguments = parser.parse_args(sys.argv[1:])
	#Convert parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	command = arguments.pop("command")
	
	print arguments
	if command == "put":
		name, snippet = put(**arguments)
		print ("Stored {!r} as {!r}".format(snippet, name))
	elif command == "get":
		name = get(**arguments)
		print ("Retrieved snippet {!r}".format(name))

if __name__ == "__main__":
	main()