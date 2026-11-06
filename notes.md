!!!!!!!!!!!The information gain is only applied to the DAG of term type rn.
!!!!!!!!!!!We can cover 1. the value to the term type 2. the item new topic
!!!!!!!!!!!Taxonomy is ontology that keeps only term type, value, and is-a
1. Simulation, 100 random messages
2. Term type and values. (Term types are just another level of values). Need to be retrievable.
3. Classifier and modifier. 
4. Input — stream of chat. Look at the input and refine the system. 
5. Scale. Number of step for classification. (The) (logN) measure it.  Compare with google? (Measurement). How fast is it retrievable. Walk thru the is-a path, the retrieve speed should be fast. 
    Scale it with traditional machine learning method.  
6. When retrieve the message. Rug pull — crypto crime (need to be accurate)  
7. Demand led concept. 
8. Pipeline 
9. ********For the new term type from LLM, we need the weights assigned by the LLM, just as (task B). And when the new value becomes term types. We need weights as well. 
10. ********When doing the optimization, the three objectives need to be measured in graph setting
11. ********Synthesize the input and output to measure the performance of the engine 
12. Is-a relation is important in retrieval speed. !!!! Use experiment to compare the retrieval speed. 
13. ******The item tagged should carry a dimensional vector for text embedding, for new value discovery and value promotion?(sentence-transformers model: It maps sentences & paragraphs to a 384 dimensional dense vector space and can be used for tasks like clustering or semantic search.)
14. *******Residual fraction: new term type. 
15. *******Limitation: we only collect limited corpora from the DLT area. The future research can spand the DAG to larger areas to test if the DAG bitset speeds more. DAG not big enough
16. *******LLM interaction on query It is the model option of the query command, implemented in taxonomy/retrieval/query.py.

python -m taxonomy.retrieval.query --text "rug pull scam on a decentralised exchange" --llm
The request goes in one call to Haiku 5.5 by default. The call runs at low effort with thinking off and a 300-token output cap.
The system prompt has two parts. A short instruction says to translate the request into a boolean query using only catalogue ids and value labels, and to answer with the query string only. The second part is the tagger's catalogue block: every term type with its question, its values and definitions, and its weighted is-a parents. That block is cached for an hour, so repeat calls are cheap.
The reply is stripped of whitespace and backticks and printed as the routed query. It then goes into the normal search, so ranking, expansion and facets run as they would for a typed query.
17. 