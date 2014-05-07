tripletriadterminal
===================

Play Triple Triad in your terminal.

For those unfamiliar, Triple Triad is a hugely addictive card game / sidequest in Final Fantasy VIII.  This wiki article is a pretty good place to read up on the game and the rules: http://finalfantasy.wikia.com/wiki/Triple_Triad

I got bored and decided I wanted to code up my own version one evening.

So far, all it does is let you play against a very dumb computer opponent.  Future TODOs for next time I get bored:

- display opponent's hand
- display hands in a more sensible fashion
- make the computer more clever than rand()
- forbid impossible card selections / moves
- add new rules
- make the board an object; we use the "flat board" function errywhere
- edit out the hardcoded 3x3 stuff, allow arbitrary board size
- make cards.txt an arg, make it a default rather than hardcoded in
- better turn handling
