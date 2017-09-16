# RDFMongoLoader
This program takes a TTL file as input and store the triples in mongoDB as documents.

# How is the conversion done?
Each entry in the TTL file will be a document in a Mongo Collection. For example, the entry:
```
ns2:98570af6-b237-4cdd-b555-98fe3de26ef8
        a                   skosxl:Label ;
        esco:hasLabelRole   ns9:neutral , ns9:male , ns9:female ;
        skosxl:literalForm  "particleboard machine technician"@en .
```        
will be stored in mongo as:

```
{
	"_id" : ObjectId("59bd4641e052453897ad22fe"),
	"source" : "ns2:98570af6-b237-4cdd-b555-98fe3de26ef8",
	"semantic" : {
		"a" : "skosxl:Label",
		"skosxl:literalForm" : "\"particleboard machine technician\"@en ",
		"esco:hasLabelRole" : [
			"ns9:neutral",
			"ns9:male",
			"ns9:female"
		]
	}
}
```
# Query the data
In the web semantic terminology, the source ID of the subject is present in an attribute called "source". The things that are said about the subject (predicate -> object) are present in the "semantic" map, in which the key is the predicate and the value could be a single object or a list of objects.
```
> db.turtle.find({source: 'ns2:98570af6-b237-4cdd-b555-98fe3de26ef8'}).pretty()
{
	"_id" : ObjectId("59bd4641e052453897ad22fe"),
	"source" : "ns2:98570af6-b237-4cdd-b555-98fe3de26ef8",
	"semantic" : {
		"a" : "skosxl:Label",
		"skosxl:literalForm" : "\"particleboard machine technician\"@en ",
		"esco:hasLabelRole" : [
			"ns9:neutral",
			"ns9:male",
			"ns9:female"
		]
	}
}
```
