% === Common Genres ===

common_genre(M1, M2, G):-
  genre(M1, G),
  genre(M2, G),
  M1\=M2.

shared_genres(M1, M2, L):-
  findall(G, common_genre(M1, M2, G), L).

genre_similarity_score(M1, M2, S) :-
  shared_genres(M1, M2, L),
  length(L, N),
  S is min(N, 4).




% === Same Director ===
same_director(M1, M2) :-
  director_name(M1, D),
  director_name(M2, D),
  M1\=M2.


% === PLot Keywords ===

common_plot_keyword(M1, M2, K):-
  plot_keyword(M1, K),
  plot_keyword(M2, K),
  M1 \= M2.

shared_plot_keyword(M1, M2, L) :-
  findall(K, common_plot_keyword(M1, M2, K), L).

plot_similarity_score(M1, M2, S):-
  shared_plot_keyword(M1, M2, L),
  length(L, N),
  S is min(N, 6).


% === actors ===


% Actor A appears in movie M
movie_actor(M, A) :- actor_1_name(M, A).
movie_actor(M, A) :- actor_2_name(M, A).
movie_actor(M, A) :- actor_3_name(M, A).

% Check for shared actor (in any position)
common_actor(M1, M2, A) :-
    movie_actor(M1, A),
    movie_actor(M2, A),
    M1 \= M2.

shared_actors(M1, M2, L) :-
    findall(A, common_actor(M1, M2, A), L).

actor_similarity_score(M1, M2, S) :-
    shared_actors(M1, M2, L),
    length(L, S).



% === decade ===

extract_year(Movie, Y) :-
    release_date(Movie, Date),
    sub_atom(Date, 0, 4, _, YearStr),
    atom_number(YearStr, Y).

decade(Movie, D) :-
    extract_year(Movie, Y),
    D is (Y // 10) * 10.

same_decade(M1, M2) :-
    decade(M1, D),
    decade(M2, D),
    M1 \= M2.



% === language ===

same_language(M1, M2) :-
    language(M1, L),
    language(M2, L),
    M1 \= M2.



% === similarity rules ===


% Exactly 1 genre and at least 1 plot keyword
find_sim_1(X, Y) :-
  genre_similarity_score(X, Y, Gscore),
  Gscore >= 1,
  plot_similarity_score(X, Y, Pscore),
  Pscore >= 1.

% Exactly 2 genres and exactly 2 plot keywords, same decade
find_sim_2(X, Y) :-
  genre_similarity_score(X, Y, Gscore),
  Gscore >= 2,
  plot_similarity_score(X, Y, Pscore),
  Pscore >= 2,
  same_decade(X, Y),
  X \= Y.

% 2 genres, 2 plot keywords, 1 shared actor, same decade
find_sim_3(X, Y) :-
  genre_similarity_score(X, Y, Gscore),
  Gscore >= 2,
  plot_similarity_score(X, Y, Pscore),
  Pscore >= 2,
  actor_similarity_score(X, Y, A),
  A >= 1,
  same_decade(X, Y),
  X \= Y.


% 2 genres, 2 plot keywords, 1 shared actor, same director, same decade
find_sim_4(X, Y) :-
  genre_similarity_score(X, Y, Gscore),
  Gscore >= 2,
  plot_similarity_score(X, Y, Pscore),
  Pscore >= 2,
  actor_similarity_score(X, Y, A),
  A >= 1,
  same_director(X, Y),
  same_decade(X, Y),
  X \= Y.


% 2 genres, 2 plot keywords, 1 shared actor, same director, same language, same decade
find_sim_5(X, Y) :-
  genre_similarity_score(X, Y, Gscore),
  Gscore >= 2,
  plot_similarity_score(X, Y, Pscore),
  Pscore >= 2,
  actor_similarity_score(X, Y, A),
  A >= 1,
  same_director(X, Y),
  same_language(X, Y),
  same_decade(X, Y),
  X \= Y.