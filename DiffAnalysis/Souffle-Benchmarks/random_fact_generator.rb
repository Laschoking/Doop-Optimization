
# --- a script to generate random fact files ---

# get some parameters from the command line
if (ARGV.length < 3 ) then
    puts "Usage: random_fact_generator.rb <seed> <num_rows> [max_value_c1, max_value_c2, ...]"
    exit 1
end
#by increasing C=max_value we get more terms that are not so connected -> this changes density

# read sead and number of entries
# maybe change seed to random?
seed = ARGV[0].to_i(36) 
num_rows = ARGV[1].to_i()

# read the value distribution
dist=[]
(ARGV.length-2).times do |i|
    dist << ARGV[i+2].to_i
end
#print(dist)
#echo dist
# the dist value $C gives the maximum value of the generated term
# thus, if $C >> $N the database is weakly conncected
# since we use a different seed, for same input might be some variation

# seed the random number generator (to get reproducable results)
#srand (Random.new_seed)
srand Random.new_seed

# data generation
num_rows.times do |i|

    # print a record
    dist.length.times do |i|

        # print a value
        print rand(dist[i])

        print "\t" unless i+1 == dist.length
    end

    # finish with a new-line
    puts 
end


