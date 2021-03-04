// Create Collections.
db.createCollection("users")
db.createCollection("collections")
// db.createCollection("cards") // Use only if collections are too large.

// Create indexes.
db.users.createIndex( { email: -1})
db.users.createIndex( { username: -1})
// db.cards.createIndex( { collection: -1}) // Use only if collections are too large.