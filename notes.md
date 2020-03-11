# Blockchain

- blockchain solves the trust issue because it uses cryptography to make sure that the authentication

## Anatomy of a Blockchain

- timestamp
- transaction information: usually amount of money
- hash to the previous block in the chain
- going forwards is easy, going backwards is extremely difficult
- the hash on the genesis block is usually manual or arbitrary
- index in the chain
- proof of work

## Proof of Work

- originally created to combat spam emails
- an arbitrarily difficult problem that is solved by spending a lot of computational time
- inversion of a hash function SHA-256 agorithm
- makes it expensive to validate data at a distributed consensus
- finding leading 0's is the proof work
- a node can die if miners decided to stop mining at it
- only real way to alter a previous chain is to spend as much computation as all of the other miners

## Proof

- if someone submits a proof before you, no credit is given
- reconstructing a blockchain basically requires cryptographic computing power of everyone else that built up the chain

## Flask Auto Restart

1. make a .env file
2. `pipenv install` if you haven't already and open up `pipenv shell`, `pipenv shell` also automatically loads up any environment variables it finds in the directories `.env`, but since it's empty, it won't load any
3. You can use Flask's CLI tool to run the app, type in `flask` to see all options
4. Specifically you are interested in `flask run`

   - initially it will error out because you need to set your `.env` variables correctly
   - See steps 5/6

5. `FLASK_ENV` will automatically default to production, which you can verify in the terminal output anytime you run a Flask app

   - setting `FLASK_ENV` to `development` will tell Flask to auto restart the app when code changes
   - eg. `FLASK_ENV='development'` in your `.env`

6. `FLASK_APP` is the environment variable that takes a path to the file you want to run

   - eg. `FLASK_APP='./basic_block_gp/blockchain.py` in your `.env`
   - basically the same as putting `python ./basic_block_gp/blockchain.py`, but it will auto run everytime Flask detects code has changed

7. WARNING: It does mean that if you want to run another file (eg running tonight's project instead of the guided project), you will need to change the `FLASK_APP` in your`.env` again, and reload the environment variables by exiting your `pipenv shell` (eg Step 2)

   - Does anyone know how to have flask specifically point to new apps?
   - I'm assuming due to the uncommon directory structure of this repo with multiple Flask apps

- Flask might give you a warning to install `python-dotenv` however, `pipenv shell` already loads the environment variables found in a `.env` into the shell it creates for you, so you don't really need `python-dotenv`
