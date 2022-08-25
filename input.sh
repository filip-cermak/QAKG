# RACE
curl http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz --output RACE.tar.gz
tar -xf  'RACE.tar.gz'

# RACE-C
curl -L -O https://github.com/mrcdata/race-c/raw/master/data.zip
unzip -qq data.zip

# Race++
mv data/train/ RACE/train/college
mv data/test/ RACE/test/college
mv data/dev/ RACE/dev/college