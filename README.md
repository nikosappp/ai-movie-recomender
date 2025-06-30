# Description

This project is a logic-based movie recommendation system built on symbolic AI principles using Prolog and Python

# How it works

## Knowledge Representation
All movie information (genres, directors, actors, plot keywords, etc.) is stored as structured Prolog facts.

## Symbolic Reasoning
Similarity rules (find_sim_1 to find_sim_5) are written in Prolog to define how two movies are considered "similar" based on shared attributes. The rules are hierarchical in strictness, find_sim_5 is the strictest while find_sim_1 is the most relaxed



