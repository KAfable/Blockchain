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
