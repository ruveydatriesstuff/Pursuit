To run CHILDES simulations:

1.  Near the top of each model script there is a choice to load either "Testing" or "Training"... just comment out the one
 you don't want to use.

2.  Load the appropriate model script.

3.  For Fazly and X-sit models, there is no random variation in output, so just run the function "simulate()" to see the
lexicon output by the model with those parameter values.

4.  For Pursuit and PV, you should average over many simulations, in which case you should use the function "meta_aggregate(n)"
where n is the number of simulations you want.