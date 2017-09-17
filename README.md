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
In the web semantic terminology, the source ID of the subject is present in an attribute called "source". The things that are said about the subject (predicate -> object) are present in the "semantic" map, in which the key is the predicate and the value could be a single object or a list of objects. You will find the tuples in a collection called "turtle".
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
The prefixs can be found in a collection called "prefix":
```
> db.prefix.find().pretty()
{
	"_id" : ObjectId("59beded8e0524515b6088fec"),
	"owl" : "<http://www.w3.org/2002/07/owl#>",
	"esco" : "<http://data.europa.eu/esco/model#>",
	"dcat" : "<http://www.w3.org/ns/dcat#>",
	"at" : "<http://publications.europa.eu/ontology/authority/>",
	"org" : "<http://www.w3.org/ns/org#>",
	"iso-thes" : "<http://purl.org/iso25964/skos-thes#>",
	"skos" : "<http://www.w3.org/2004/02/skos/core#>",
	"skosXl" : "<http://www.w3.org/2008/05/skos-xl#>",
	"rov" : "<http://www.w3.org/ns/regorg#>",
	"rdfs" : "<http://www.w3.org/2000/01/rdf-schema#>",
	"prov" : "<http://www.w3.org/ns/prov#>",
	"ns18" : "<http://data.europa.eu/esco/structure/>",
	"rdf" : "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
	"ns12" : "<http://data.europa.eu/esco/regulated-professions/>",
	"ns13" : "<http://data.europa.eu/esco/relationship-type/>",
	"ns10" : "<http://data.europa.eu/esco/skill/>",
	"ns11" : "<http://data.europa.eu/esco/occupation/>",
	"ns16" : "<http://data.europa.eu/esco/relation/>",
	"ns17" : "<http://data.europa.eu/esco/concept-scheme/>",
	"ns14" : "<http://data.europa.eu/esco/skill-reuse-level/>",
	"ns15" : "<http://data.europa.eu/esco/skill-type/>",
	"foaf" : "<http://xmlns.com/foaf/0.1/>",
	"ns2" : "<http://data.europa.eu/esco/label/>",
	"dc" : "<http://purl.org/dc/elements/1.1/>",
	"ns9" : "<http://data.europa.eu/esco/label-role/>",
	"qdr" : "<http://data.europa.eu/esco/qdr#>",
	"ns1" : "<http://www.w3.org/2008/05/skos-xl#>",
	"dct" : "<http://purl.org/dc/terms/>",
	"ns3" : "<http://data.europa.eu/esco/labels/>",
	"ns4" : "<http://data.europa.eu/esco/skill-type/knowledge/label/>",
	"ns5" : "<http://data.europa.eu/esco/model#>",
	"ns6" : "<http://data.europa.eu/esco/node-literal/>",
	"ns7" : "<http://data.europa.eu/esco/isco/>",
	"skosthes" : "<http://purl.org/iso25964/skos-thes#>",
	"adms" : "<http://www.w3.org/ns/adms#>",
	"euvoc" : "<http://publications.europa.eu/ontology/euvoc#>",
	"xsd" : "<http://www.w3.org/2001/XMLSchema#>",
	"skosxl" : "<http://www.w3.org/2008/05/skos-xl#>",
	"ns22" : "<http://purl.org/iso25964/skos-thes#>",
	"ns21" : "<http://data.europa.eu/esco/Notation/>",
	"ns20" : "<http://purl.org/dc/terms/>"
}

```
# Configuration
Edit the rdfmongoloader.cfg with the appropriate configuration.

## basic
#### ttl_file
Absolute path of the TTL file
#### batch_size
Integer greater that 0 which represents the size of the batch of entries in the TTL file.

## mongo
#### name
Name of the Mongo database
#### Host
Mongo hostname
#### Port
Mongo port

# Execute it
Just go inside the source folder and run it with:
```
python __main__.py
```
