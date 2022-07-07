import requests
from bs4 import BeautifulSoup
from random import choice
#from time import sleep

all_quotes=[]
base_url="http://quotes.toscrape.com"
url="/page/1"

while url:
	res=requests.get(f"{base_url}{url}")
	soup=BeautifulSoup(res.text,"html.parser")
	quotes=soup.find_all(class_="quote")
	#print(quotes)

	for quote in quotes:
		all_quotes.append({
			"text":quote.find(class_="text").get_text(),
			"author":quote.find(class_="author").get_text(),
			"bio-link":quote.find("a")["href"]
		})
	next_btn=soup.find(class_="next")
	url=next_btn.find("a")["href"] if next_btn else None
	#sleep(2)

def start_game():
	quote = choice(all_quotes)
	remaining_guess=4
	print("Here a quote: ")
	print(quote["text"])
	#print(quote["author"])
	guess=""
	while guess.lower() != quote["author"].lower() and remaining_guess>0:
		guess=input(f"Who said this quote? Guess Remaining: {remaining_guess}\n")
		if guess.lower()== quote["author"].lower():
			print("You got it right !!")
			break
		remaining_guess -= 1
		if remaining_guess==3:
			res=requests.get(f"{base_url}{quote['bio-link']}")
			soup=BeautifulSoup(res.text,"html.parser")
			birth_date=soup.find(class_="author-born-date").get_text()
			birth_place=soup.find(class_="author-born-location").get_text()
			print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
		elif remaining_guess==2:
			print(f"Here's a hint: The author's first name starts with : {quote['author'][0]}")
		elif remaining_guess==1:
			last_initial=quote['author'].split(" ")[1][0]
			print(f"Here's a hint: The author's last name starts with : {last_initial}")
		else:
			print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
			
	again=""
	while again.lower() not in ("y","n","yes","no"):
		again= input("Play Again (y/n)?")
	if again.lower() in ("yes","y"):
		return start_game()
	else:
		print("bye")

start_game()


