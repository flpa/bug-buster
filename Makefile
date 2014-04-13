clean:
	rm -f *.pyc
	rm -f bugbuster.zip
zip:	clean
	zip -r bugbuster.zip . -x ".git*"	
