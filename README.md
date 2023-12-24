# Recipe-book
Recipe-book django web application

features and functionalities:
- sign-in
- create new recipe (puplic or privte option)
- edit my recipes
- delete my recipes
- share my recipes on social media
- view my recipes with filtering options
- view other user's recipes (if puplic) with filtering options( even if not a user)
- comment others recipes
- rate others recipes
- add others recipes to your favorites list
- be notified when others comment on your recipes 
- replay to comments on your recipes

database:
tables:
- users:
	- id - pk
	- username
	- email
	- password
- recipes:
	- id pk
	- recipe-name 
	- category
	- img
	- user-id - fk
	- ingrediants
	- directions
	- public boolean
- comments:
	- id pk
	- recipe-id - fk
	- user-id - fk
	- comment-text
	- replay boolean
	- original-comment-id  default = null
- ratings
	- recipe-id - fk
	- recipe rating smallint (1 to 5)

