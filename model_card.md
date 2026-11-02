# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Imagine a friend who knows your taste and is flipping through a stack of songs. For each song, they ask five questions and give it points for each:

1. **Is the energy about right?** If you want mellow music, a calm song earns nearly full points and a loud, intense one earns few. The goal is *closeness* to what you want, not "more is better."
2. **Does the mood match?** If you asked for "chill" and the song is "chill," it gets full points. Otherwise it gets none.
3. **Is the positivity (how happy or upbeat it sounds) about right?** Closeness again.
4. **Is it your favorite genre?** Full points for a match, none otherwise.
5. **Is the amount of acoustic sound about right?** Closeness again. Do you like acoustic guitars and pianos, or electronic sounds?

Not every question counts equally. Energy matters most, then mood, then positivity, then genre, and acoustic sound matters least. Mood counts a little more than genre because it describes how a song *feels*, and the catalog is too small for many songs to share a genre.

The friend adds up the points to get a score between 0 and 1, where 1 is a perfect match. Once every song has a score, they line the songs up from highest to lowest and hand you the top five. If two songs tie, the one with the matching mood goes first. Each recommendation also comes with a short note on where its points came from, such as "mood match, energy close," so you can see *why* it was picked.

This is a **content-based** approach: it only looks at the songs' own traits and your stated preferences. It does not use other listeners' habits, so it can't say "people like you also enjoyed this."

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
