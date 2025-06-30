import pandas as pd 
csv_file = "movies_metadata.csv"
data = pd.read_csv(csv_file, encoding="utf-8")
data = data.astype(str).fillna("unk")

# Text cleaner for safe Prolog atoms

def clean_text(text):
    text = str(text)
    return (
        text.strip()
        .lower()
        .replace('\xa0', '')
        .replace('\n', '')
        .replace('\t', '')
        .replace("'", "")
        .replace('"', "")
        .replace("’", "")
        .replace("“", "")
        .replace("”", "")
        .replace(" ", "_")
        
    )


facts = []

for row in data.itertuples(index=True, name='Pandas'):
    movie_title = clean_text(row.movie_title)

    # Budget
    budget = str(row.budget).strip()
    if budget.isdigit():
        facts.append(f"budget('{movie_title}','{budget}').")

    # Genres
    for genre in row.genres.split("|"):
        genre = clean_text(genre)
        if genre and genre != "unk":
            facts.append(f"genre('{movie_title}','{genre}').")

    # Homepage
    homepage = str(getattr(row, 'homepage')).strip()
    homepage_clean = homepage.replace("'", "").replace('"', '')
    if homepage and homepage.lower() != "unk":
        facts.append(f"homepage('{movie_title}','{homepage_clean}').")

    # Movie ID
    id = str(row.id).strip()
    if id.isdigit():
        facts.append(f"movie_id('{movie_title}','{id}').")

    # Plot Keywords
    for plot_keyword in row.plot_keywords.split("|"):
        plot_keyword = clean_text(plot_keyword)
        if plot_keyword and plot_keyword != "unk":
            facts.append(f"plot_keyword('{movie_title}','{plot_keyword}').")

    # Language
    language = clean_text(row.language)
    if language and language != "unk":
        facts.append(f"language('{movie_title}','{language}').")

    # Original Title
    original_title = clean_text(row.original_title)
    if original_title and original_title != "unk":
        facts.append(f"original_title('{movie_title}','{original_title}').")

    # Overview 
    overview = str(row.overview).strip()
    if overview and overview.lower() != "unk":
        overview_clean = overview.replace("'", "").replace('"', '').replace("\n", " ")
        facts.append(f"overview('{movie_title}','{overview_clean}').")

    # Popularity
    popularity = str(row.popularity).replace(".", "").strip()
    if popularity.isdigit():
        facts.append(f"popularity('{movie_title}','{popularity}').")

    # popularity(movie, "120000000").   % This is a string (atom), not a number
    # not the form we want because we might compare the values later to recomend
    # but this: facts.append(f"popularity({movie_title},{popularity_clean}).")
    # creats this: popularity(inception, 120000000). Prolog sees this as a number

    # Production Companies
    import ast
    try:
        companies = ast.literal_eval(row.production_companies)
        for company in companies:
            name = clean_text(company.get('name', 'unk'))
            #dictionary.get(key, default_value)
            #key: what you're trying to look up
            #default_value: what to return if the key is not found
            if name != "unk":
                facts.append(f"production_company('{movie_title}','{name}').")
    except:
        pass

    # Production Countries
    try:
        countries = ast.literal_eval(row.production_countries)
        for country in countries:
            name = clean_text(country.get('name', 'unk'))
            if name != "unk":
                facts.append(f"production_country('{movie_title}','{name}').")
    except:
        pass

    # Release_date
    release_date = str(row.release_date).strip()
    release_date = clean_text(release_date)
    if release_date and release_date!="unk":
        facts.append(f"release_date('{movie_title}','{release_date}').")

    # Gross
    gross = str(row.gross).strip()
    if gross.isdigit():
        facts.append(f"gross('{movie_title}','{gross}').")

    # Duration
    duration_raw = str(row.duration).strip()
    if duration_raw.lower() != "unk":
        try:
            duration = int(float(duration_raw))
            facts.append(f"duration('{movie_title}','{duration}').")
        except:
            pass


    # Spoken Languages
    try:
        spoken_languages = ast.literal_eval(row.spoken_languages)
        for lang in spoken_languages:
            name = clean_text(lang.get('name', 'unk'))
            if name != "unk":
                facts.append(f"spoken_language('{movie_title}','{name}').")
    except:
        pass

    # Status
    status = clean_text(row.status)
    if status and status != "unk":
        facts.append(f"status('{movie_title}','{status}').")

    # Tagline
    tagline = clean_text(row.tagline)
    if tagline and tagline != "unk":
        facts.append(f"tagline('{movie_title}','{tagline}').")

    # Vote Average
    vote_average = str(row.vote_average).strip()
    vote_average = float(vote_average)
    facts.append(f"vote_average('{movie_title}','{vote_average}').")

    # Num Voted Users
    num_voted = str(row.num_voted_users).strip()
    if num_voted.isdigit():
        facts.append(f"num_voted('{movie_title}','{num_voted}').")

    # Country
    country = str(row.country).strip()
    if country and country != "UNK":
        facts.append(f"country('{movie_title}','{country}').")

    # Director
    director_name = clean_text(str(row.director_name).strip())
    if director_name and director_name != "unk":
        facts.append(f"director_name('{movie_title}','{director_name}').")

    # Actor_1
    actor_1_name = clean_text(str(row.actor_1_name).strip())
    if actor_1_name and actor_1_name != "UNK":
        facts.append(f"actor_1_name('{movie_title}','{actor_1_name}').")

    # Actor_2
    actor_2_name = clean_text(str(row.actor_2_name).strip())
    if actor_2_name and actor_2_name != "UNK":
        facts.append(f"actor_2_name('{movie_title}','{actor_2_name}').")
    
    # Actor_1
    actor_3_name = clean_text(str(row.actor_3_name).strip())
    if actor_3_name and actor_3_name != "UNK":
        facts.append(f"actor_3_name('{movie_title}','{actor_3_name}').")


# Saving facts to a .pl

with open("movie_facts.pl", "w", encoding="utf-8") as f:
    for fact in sorted(facts):
        f.write(fact + "\n")
