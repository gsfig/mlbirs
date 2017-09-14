#!/bin/bash

###############################################################################
#                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License"); you may     #
# not use this file except in compliance with the License. You may obtain a   #
# copy of the License at http://www.apache.org/licenses/LICENSE-2.0           #
#                                                                             #
# Unless required by applicable law or agreed to in writing, software         #
# distributed under the License is distributed on an "AS IS" BASIS,           #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
# See the License for the specific language governing permissions and         #
# limitations under the License.                                              #
#                                                                             #
###############################################################################
#                                                                             #
# Software developed based on the work published in the following articles:   #
# - F. Couto, L. Campos, and A. Lamurias, MER: a minimal named-entity         #
#   recognition tagger and annotation server,                                 #
#   in BioCreative V.5 Challenge Evaluation, 2017                             #
#   www.biocreative.org/media/store/files/2017/BioCreative_V5_paper18.pdf     #
#                                                                             #
# @authors F. Couto, L. Campos, and A. Lamurias                               #
###############################################################################

SAVEIFS=$IFS; IFS=$(echo -en "");

# set -x #debug

cd data

filename=$(basename $1 .txt)

egrep '[[:alpha:]]{3,}' $filename.txt >  $filename.aux1
egrep -v '[[:digit:]]{5,}' $filename.aux1 >  $filename.aux2

sed -e 's/^ *//' -e 's/ *$//' $filename.aux2 > $filename.aux3 # remove leading and trailing whitespace
sed -e 's/[[:space:]]\+/ /' $filename.aux3 >  $filename.aux4 # remove multiple whitespace
awk '!a[$0]++' $filename.aux4 > $filename.aux5 # remove duplicate lines

echo '================'
sed 's/[^[:alpha:][:digit:][:space:]]/./g' $filename.aux5 | tr '[:upper:]' '[:lower:]' > $filename.aux

egrep '^[^ ]*$' $filename.aux > $filename'_word1.txt'
tail $filename'_word1.txt'
echo '================'

egrep '^[^ ]+ [^ ]+$'  $filename.aux > $filename'_word2.txt'
tail $filename'_word2.txt' 
echo '================'

egrep ' [^ ]+ ' $filename.aux > $filename'_words.txt' 
tail $filename'_words.txt' 
echo '================'

egrep -o "^[^ ]+ [^ ]+"  $filename'_words.txt' | awk '!a[$0]++' > $filename'_words2.txt'
tail $filename'_words2.txt' 
echo '================'

rm -f $filename.aux*