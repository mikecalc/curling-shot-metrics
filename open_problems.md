# Ten Open Problems 

This project reads the shot-by-shot pages of World Curling's results books into data: for 4,150 international games since 2013, where every stone was after every shot, who threw it, what was called and how it was graded, and how each end and game came out. On top of that data sits a way of valuing positions and shots, **Points Gained**: for any position it estimates what the end is likely to produce, given how teams at that level have played from similar positions, and it values each shot by how much it changed that expectation. The shot's value is split into the part that came from the call and the part that came from the execution.

Working with the data has turned up questions we cannot answer yet, or which expose limitations of the model (for a variety of reasons, including lack of enough data). We list ten here, roughly in the order we run into them, in the hope that curlers, coaches and analysts can participate in the discussion and contribute. The list will change as the data grows and the work moves on.

The project, its data and its code are at https://github.com/mikecalc/curling-shot-metrics.

---

## 1. What is an early-end position worth?

Late in an end, the model reads positions well: with a rock or two left it knows the likely outcomes. Early in an end it knows little. With twelve or more rocks to come, it does barely better than knowing only who has hammer and the score. Either the early end is genuinely hard to predict, because so much can still happen, or we are describing early positions in the wrong terms. A corner guard, a centre guard and a stone in the rings mean something to a skip long before the end is decided, and the model does not yet see all of it.

This matters most for leads and seconds, whose stones are thrown when the end is least decided. We have made their shot values more stable. Each stone is now judged against a nearer horizon, a couple of stones ahead, rather than the end's final score. But we have not made the early positions themselves better understood.

## 2. Can the data learn the words skips use?

Skips talk in configurations: a split house, the deuce is loose, the steal is on, a runback is there. We wrote tests for several of these by hand, with thresholds chosen by curling judgement. Some thresholds hold up in the data and some needed correcting. A split house with two stones side by side at the same depth is almost never doubled off (about 2% of the time at four to six feet apart); the same pair staggered in depth comes off seven times as often. Separation alone, which was our first definition of a split, misses that.

Could the data discover this vocabulary on its own, by finding positions that play out alike and that leave the opponent the same kinds of options? If it rediscovered the configurations skips already name, that would be reassuring; if it found ones nobody names, that would be interesting.

## 3. What was the best call, and how good is a skip's calling against it?

Today a call is compared with what the field usually calls from that position. That tells us when a skip does something unusual, not whether it was right. The 2026 Olympic men's final is the example we keep coming back to: down one with hammer in the ninth end, Brad Jacobs called a runback through traffic that scored three. The field rarely calls that shot from there, because most teams do not make it often enough. Was it the best call on the sheet for him?

Answering that needs four things: whether the shot was really there (the geometry), what the ice allows, how often this thrower makes it (the skill), and what each outcome is worth in this game (the score and ends left). The ice is as much a part of the geometry as the stones: in the same way the angle decides whether a take-out is on, how much the ice curls decides how makeable a come-around or a chip is, and swingy ice and straight ice offer different menus from the same position. Skips also plan across several stones, managing the risk of a big miss that may play out over the rest of the end. A best call is not a single shot.

## 4. How do strategy and execution depend on each other?

A call's value depends on who throws it. A shot with a bad miss is a poor call for a team that misses it often and a good one for a team that rarely does. There are signs of this in the data: the best teams call shots whose worst outcomes are as bad as anyone's, and then produce those worst outcomes less often than the field. It is as if they know which part of the risk does not apply to them.

The difficulty is circular. To say whether a call was right for a team, we need to know how that team executes; to judge the execution, we need to know what was called and why. Pulling "the right call for this team" apart from "the right call for the field" without the measurement feeding on itself is an open problem.

## 5. Can the diagrams tell us how shots are actually missed?

The results books mark the delivered stone and show where struck stones were before the shot. Across hundreds of thousands of shots, that is a record of how draws come to rest relative to where they seem to have been aimed, and which stone a hit actually struck. It is a record of execution error by shot type, turn, level and position.

With a good model of how shots are missed, the shots that were not called could be simulated, and that is what problem 3 needs. The difficulty is that the target of a shot is not recorded, only where the stone ended up, and inferring the target from the result mixes the aim with the miss.

## 6. How hard is a shot that was not called?

Make rates in the data describe shots as they were chosen, not shots in general. A runback at an angle looks no harder than a straight one in the data, but that is because skips only call the angled runback when it is on. The shots teams decline are missing from the record, and they are the hard ones.

A fair measure of difficulty needs the positions where a shot was available but not called: how often it was declined, and what was called instead. The data holds every position; the problem is deciding when a shot counts as available.

## 7. Can the model learn the rare situations that decide games?

The positions that decide games are rare, and rare positions are the hardest for a model to learn. Two examples from the data. In a tied last end with hammer, when a peel leaves both guards in place, the team without hammer goes on to steal 30% of the time; the model expects 23%, so it barely charges the missed peel. With a single steal stone in front of two or more of the hammer team's, a guard placed close in front, where a runback is easy, left the hammer team better off than a guard placed long; the model has it the other way round. Each of these is a few hundred ends in a corpus of tens of thousands.

## 8. How do we compare players across different fields?

A good shot at the Olympics and a good shot at the World Juniors are measured against different fields. Today each event is its own yardstick, which keeps comparisons fair within an event and makes them hard across events. Adding national championships and tour events, which we hope to do, makes the problem larger: fields of different depth, ice of different quality, and teams that meet across them.

## 9. Who gets credit for a shot?

The data records the thrower. But a shot is also the skip's call and broom, the sweepers' judgement of weight and line, and the team's read of the ice. There are signs in the data that a team's lead and second rise and fall together more than the thrower-by-thrower record explains, and sweeping and the skip's broom are the obvious candidates. The results books do not record who swept or where the broom was held.

## 10. How sure can we be?

Some of the most interesting findings rest on small samples. A skip's runback record may be forty shots over several events. Stone positions are read from the diagrams to about half an inch, and stones closer than that cannot be told apart. Player ratings, study results and leaderboards do not yet carry any measure of how much they could change with more data. Honest uncertainty would make every report more useful, and it would take some of the more exciting findings down a notch.

---

## Also on our list

How ice changes over a game and over a week, which the best call of problem 3 will eventually need: the results books do not describe the ice, so its effect has to be read from how shots behaved on it. Mixed doubles, which is a different game with its own strategy. And a way to describe a team's aggressiveness by the risks it is willing to take, rather than by the shots it calls.

Comments on any of these, and suggestions for problems we have missed, are welcome.
