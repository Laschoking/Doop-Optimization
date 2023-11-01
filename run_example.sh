#Go to doop/master:

#java to Binary:

bin/mkjar Examples/Example_1.java 1.8 Examples/Example_1.jar


#execute doop with analysis:

#./doop -a context-insensitive  -i Examples/Example_1.jar --generate-jimple  -id Example_1_con_ins --discover-main-methods --Xfacts-subset APP

#execute doop without analysis

./doop -a context-insensitive  -i Examples/Example_1.jar --generate-jimple  -id Example_1_facts_only --discover-main-methods --Xfacts-subset APP

