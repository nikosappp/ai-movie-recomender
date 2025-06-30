from pyswip import Prolog
from facts_extract import clean_text

# Initialize Prolog
prolog = Prolog()
prolog.consult("movie_facts.pl")
prolog.consult("recommendation_rules.pl")

user_input = input("Enter a movie title: ")
target_movie = clean_text(user_input)

results_by_level = {}
seen_movies = set()

for level in range(5, 0, -1):
    sim_fun = f"find_sim_{level}"
    query_str = f"{sim_fun}('{target_movie}', X)"
    
    try:
        # Get only one match per similarity level
        matches = list(prolog.query(query_str, maxresult=10))
        for res in matches:
            similar_movie = res["X"]
            if similar_movie not in seen_movies:
                results_by_level[sim_fun] = similar_movie
                seen_movies.add(similar_movie)
                break  # Stop after first unique match per level
    except Exception as e:
        print(f"Error with {sim_fun}: {e}")

if results_by_level:
    print(f"\nMovies similar to '{user_input}':\n")
    # Print in descending similarity order
    for sim_rule in sorted(results_by_level.keys(), reverse=True):
        print(f"- {results_by_level[sim_rule]} (matched by: {sim_rule})")
else:
    print(f"\nNo similar movies found for '{user_input}' using any rule.")
