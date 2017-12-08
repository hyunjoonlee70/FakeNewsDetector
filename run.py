# program that runs all.
import os
from signal import signal, SIG_IGN, SIGPIPE
from flask import Flask, request

app = Flask(__name__)
@app.route("/")


def main():
	url = request.url.replace("%2F", "/")
	# url includes parts of the original url that
	# a user wanted to check. Used the fact that
	# after "?" the rest of the url won't be read.
	url =  url[23:]
	fd = open("url.txt", "w")
	fd.write(url)
	print url
	fd.close()
	# equivalent to calling these in the terminal.
	os.system("python pageExtractor.py")


if __name__ == '__main__':
    main()
