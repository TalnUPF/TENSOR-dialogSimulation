# TENSOR-dialogSimulation
Repository with utils to analyze chat data generated in Tensor.

- raw/ contains the input xml that is generated via Spark.
- dicts/ contains basic dicts to get to know the domain concept usage.
- out/ contains the generated outputs
- seeds/ has the basic topic seeds
- dictSeeds/ has the most important tokens of each seed
- annotationWeb/ has an html page where the users can annotate how well our system is doing, to see it, just copy that into your var/www/html and access localhost/chatEval 
- build/ contains the files needed to generate a Docker with the demo.

The other folders are just probably iterations of other content.

- chatFeatures.py opens an input xml, fills the data structures and computes basic features.
- createDB.sql is a script that creates a mysql table to store word embeddings.
- sqlEmbeddings.py is the class that manages the retrieval and operations with word embeddings.
- date.py uses all of the computed features and generates a report.
- role.py analyzes the role of the users of the chats.
- utils.py is a script that helps with PoS tagging, tokenizing, etc. Uses Spacy
- topic.py computes day relevance and topic clustering.


