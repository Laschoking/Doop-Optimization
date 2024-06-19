# !bin/bash
doop=/home/kotname/Documents/Diplom/Code/doop/master
db1=ForLeft
db2=ForRight

# diff facts
facts=$doop/facts.txt

cd $doop

#bin/mkjar ../../cpec-doop-and-jdime-experiments/jdime_application/jdime/testres/ASTBBTests/left/ForLoop.java 1.8 input/ForLeft.jar


cd $doop/out/$db1/database
# analysis facts individually
wc -l *.facts > ../summary/all-facts.txt

#cat $db1/summary/all-facts.txt | awk '$1 > 0{ print $0}'

cd $doop/out
# sum of facts 
grep -E "total" $db1/summary/all-facts.txt | awk '{print $1}'| xargs echo "number of facts in total:" 

# find non-empty tables
cat $db1/summary/all-facts.txt | awk '$1 > 0 && $2 !="total"{ print $0}' > $db1/summary/non-empty-files.txt

#output nr. of non-empty tables
wc -l $db1/summary/non-empty-files.txt| xargs echo "number of non-empty tables  (from 133) :" 

# nr. of all tables: 133
wc -l facts.txt | xargs echo "number of all tables:" 

# check for common lines of both databases (invert of diff)
for fact in $(awk '{print $2}' $db1/summary/non-empty-files.txt); do comm -12 <(sort $db1/database/$fact) <(sort $db2/database/$fact) |  wc -l | xargs echo $fact >> $db1/summary/common_lines.txt; done

# copy common lines of both databases to db2
cp $db1/summary/common_lines.txt $db2/summary/common_lines.txt

# output non-empty files & percentage of similarity

for file in $(awk '{print $1, $2}' $db1/summary/non-empty-files.txt); do echo $1 done;
