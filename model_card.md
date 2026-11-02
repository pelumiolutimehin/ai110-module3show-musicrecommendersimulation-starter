# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

  Musical Match Maker 1.0

---

## 2. Intended Use

Explain what your recommender tries to predict or suggest.

**The goal:** Suggest songs a user will probably like.

**The task:** The user gives a favorite genre, a favorite mood, and a few target numbers. These are energy, positivity, and acoustic sound. The system scores all 20 songs. It returns the top 5 with short reasons.

**What it predicts:** How well each song fits the user's taste. A score of 1 is a perfect fit. A score of 0 is a bad fit.

**What it assumes:** The user has one clear taste. They can describe it with the labels and numbers above.

**Who it is for:** Classroom exploration only. It is not built for real listeners.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**In plain language:**

Picture a friend flipping through a stack of songs for you. They give each song points on five questions:

1. **Is the energy about right?** Closer to what you want earns more points.
2. **Does the mood match?** A match gets full points. Anything else gets none.
3. **Is the positivity about right?** Closer earns more.
4. **Is it your favorite genre?** A match gets full points. Anything else gets none.
5. **Is the acoustic sound about right?** Closer earns more.

The questions don't count equally. From most to least: energy (30%), mood (25%), positivity (20%), genre (15%), and acoustic sound (10%).

The points add up to a score from 0 to 1. The friend sorts the songs from highest to lowest and gives you the top five. A tie goes to the song with the matching mood. Each song comes with a short note on where its points came from, like "mood match (+0.25)".

**What changed from the starter:** The starter returned songs in file order with no scoring. Now every song is scored and ranked, with reasons.

This is a **content-based** approach: it only looks at the songs' own traits and your stated preferences. It does not use other listeners' habits, so it can't say "people like you also enjoyed this."

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

**Size:** The catalog is one file, `data/songs.csv`. It has 20 songs. I did not add or remove any.

**What each song has:** An id, title, artist, genre, mood, energy, tempo, positivity (valence), danceability, and acoustic level. The numbers run from 0 to 1. Tempo is in beats per minute.

**What the scoring uses:** Genre, mood, energy, positivity, and acoustic level. It does not use tempo or danceability.

**What is in it:**
- 17 genres. Lofi has 3 songs and pop has 2. The other 15 genres have one song each.
- 15 moods. Chill has 3 songs. Happy, intense, and melancholic have 2 each. The rest have one.
- Energy runs from 0.22 to 0.97, so quiet and loud songs are both there.

**Limits:**
- 20 songs is tiny. A real app has millions.
- Most genres have one song, so a genre match can only help one song.
- Each song has one genre and one mood. Real songs often fit more than one.
- Many tastes are missing, such as K-pop, gospel, and country beyond one song.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

**Who it works well for:** Users whose taste fits the catalog and is clear. Chill lofi, intense rock, and high-energy pop fans all got lists that made sense.

**What the scoring gets right:**
- It finds an exact match. Each of the 20 songs ranked #1 for a profile built from its own traits.
- It handles both quiet and loud tastes. The energy score rewards being close, so low-energy and high-energy users are both served.
- Different tastes give different lists. Chill lofi and intense rock share no songs.
- It explains itself. Every song comes with reasons, like "mood match (+0.25)", so you can see why it ranked where it did.

**Where it matched my gut:**
- Chill lofi fans got Midnight Coding and Library Rain on top.
- The rock fan got Storm Runner, a perfect 1.00.
- The pop fan got Sunrise City first.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness found: all-or-nothing genre and mood matching in a small catalog.** Genre and mood are exact-match labels worth 40% of the score together, but 14 of the 17 genres in the 20-song catalog have only one song. A lofi fan has three genre matches to choose from, while a reggae or folk fan gets one boosted song and then a list ranked on numbers alone. Near-misses earn nothing: "relaxed" gets no credit for "chill", and a profile with labels the catalog lacks (like "k-pop" and "nostalgia") produced a top five scored 0.55 to 0.51, so the order is close to arbitrary. Removing the mood check changed the #1 pick for a chill lofi profile from Midnight Coding to Focus Flow, which shows how much a single label can decide the result.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

Chill lofi, relaxed lofi (the starter profile), intense rock, high-energy pop, and three stress tests: "sad but hyper" (pop and sad, but very energetic and upbeat), "ghost labels" (a genre and mood not in the catalog), and a label near-miss (the chill lofi numbers with the genre typed as `"Lo-Fi "`). Each of the 20 songs also ranks #1 for a profile built from its own traits.

### Comparing pairs of profiles

- **Chill lofi vs. intense rock:** calm acoustic lofi and ambient vs. loud electric rock, with no songs in common. Opposite tastes give opposite lists, as expected.
- **Intense rock vs. high-energy pop:** both want loud music, so both lean on energy, and the labels split them: Storm Runner (1.00) for rock, Sunrise City (0.96) for pop. Gym Hero shows up in both because it is loud, pop, and "intense".
- **Chill lofi vs. relaxed lofi:** only one song is "relaxed", a jazz song, and it ranks #1 for the lofi fan. Mood is worth more than genre, so this makes sense, but it is surprising.
- **High-energy pop vs. sad but hyper:** the lists are nearly the same. The one sad song is quiet, so the energy match outvotes the mood and the "sad" user gets upbeat pop.
- **Chill lofi vs. label near-miss:** identical numbers, but the typo costs the genre match, so the lofi songs fall from 0.98 to about 0.58.
- **Ghost labels vs. the rest:** no standout, with top scores of 0.55 to 0.51, so the order is close to arbitrary.

### What surprised me

- **Why does "Gym Hero" keep showing up for people who want "Happy Pop"?** It is a pop song that is loud and upbeat, so it earns points for genre, energy, and positivity. It only misses on mood ("intense", not "happy"), which costs 0.25, so it still scores 0.73 and lands third.
- **One mood label can swing the #1 pick.** Removing the mood check changed the top chill lofi song from Midnight Coding to Focus Flow.
- **Typing matters.** A stray capital letter or space silently removed the genre match.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. **Give partial credit for close labels.** Right now "relaxed" gets zero for "chill". I would score similar moods and genres as near matches. I would also clean up typing, like capital letters and extra spaces, so `"Lo-Fi "` still matches "lofi".
2. **Add more songs.** Twenty is too few. Most genres have one song, so a genre match helps only one song. A bigger catalog would make the genre and mood points fair for more users.
3. **Mix up the top 5.** The top results can all sound alike. I would limit how many songs from one genre can show up. I would also use tempo and danceability, which the scoring ignores today.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**What was your biggest learning moment during this project?**

My biggest learning moment during this project was seeing how much a few small choices decide the results. When I turned off the mood check, the #1 song for a chill lofi fan changed. Gym Hero kept showing up for pop fans because genre and energy gave it enough points to beat its wrong mood. One weight or one label can shape what a user sees. That showed me how bias gets in, even in a tiny program.

**How did using AI tools help you, and when did you need to double-check them?**

AI helped me move fast. It wrote the first version of `load_songs`, `score_song`, and the ranking step, formatted the output, and helped me test odd profiles. I still had to check its work.
- The `python -m src.main` command failed with an import error, and I had to understand why the two ways of running the file differ.
- Some numbers came from test profiles I made up. They show a pattern, but they are not exact.
- I needed to read the results myself to decide if they were actually good. AI can't necessarily know what a chill lofi fan wants.

**What surprised you about how simple algorithms can still "feel" like recommendations?**

I was surprised how real it felt. The program only adds up five numbers. Yet the top results for chill lofi, intense rock, and happy pop made sense. The reasons, like "mood match (+0.25)", made it feel like the system understood the user. It doesn't. It just compares labels and numbers. That showed me how easy it is to trust a list because it comes with a neat explanation.

**What would you try next if you extended this project?**

- Give partial credit for close labels, so "relaxed" counts a little for "chill".
- Add many more songs, so each genre has more than one.
- Mix up the top 5 so it doesn't repeat one genre.
- Use tempo and danceability, which the scoring ignores today.
- Let a user have more than one taste, like calm study music and loud workout music. 