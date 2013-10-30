My solution for kaggle.com competition StumbleUponEvergreen
Uses naive bayes and boilerplate to predict results

Usage:
First run StumbleUpon.R (don't forget to change path to working dir in it)
Then you'll have 2 files 'train.txt' and 'test.txt' in correct formats
Then you can just run python file (just set output filename and last flag
as False), if you want to perform some check - just write a short script, which
separetes train sample in two randomly, so you can now check solution, just
removing two last args in main() function
Good luck ;)

Update: just fixed files contents, so just run R script first, then run split.py
to get learning and testing sets. then just run analizeMod.py to check quality
then, to get output file, simply add 2 arguments at the end of function main: 
output filename and false. Remember also to change first two args!
You'll get score 0.81388. You can use analizeModCategorization.py as well,
but for now it reaches score 74.~ and is near RandomForestBenchMark.
