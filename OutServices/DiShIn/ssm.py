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
# - F. Couto and M. Silva, Disjunctive shared information between ontology    #
#   concepts: application to Gene Ontology, Journal of Biomedical Semantics,  #
#   vol. 2, no. 5, pp. 1-16, 2011                                             #
#   http://dx.doi.org/10.1142/S0219720013710017                               #
# - F. Couto and H. Pinto, The next generation of similarity measures that    # 
#   fully explore the semantics in biomedical ontologies, Journal of          # 
#   Bioinformatics and Computational Biology, vol. 11, no. 1371001,           # 
#   pp. 1-12, 2013                                                            #
#   http://dx.doi.org/10.1186/2041-1480-2-5                                   #
#                                                                             #
# @author Francisco M. Couto                                                  #
###############################################################################

import sqlite3
import math

intrinsic = False
mica = False
global connection

def semantic_base (sb_file):
    
    global connection
    connection = sqlite3.connect(sb_file)
    
def get_id (name):

    iden = 0
    
    rows = connection.execute('''
        SELECT id
        FROM entry
        WHERE name = ?
    ''', (name,))

    for row in rows:
       iden = row[0]

    return iden

def num_entries ():

    num = 0
    
    rows = connection.execute('''
        SELECT id
        FROM entry
    ''')

    for row in rows:
       num = row[0]

    return num

def common_ancestors (entry1, entry2):

    ancestors = []
    
    rows = connection.execute('''
        SELECT DISTINCT t1.entry2
        FROM transitive t1, transitive t2
        WHERE t1.entry1=? AND t2.entry1=? AND t1.entry2=t2.entry2
        ''', (entry1, entry2, ))
    
    for row in rows:
        ancestors.append(row[0])
    return ancestors


def information_content_extrinsic (entry):
    #print entry
    rows = connection.execute('''
        SELECT e.freq
        FROM entry e
        WHERE e.id = ?
        ''', (entry,))
    for row in rows:
        freq = row[0] + 1.0
    #print (freq)
    rows = connection.execute('''
        SELECT MAX(e.freq)
        FROM entry e
        ''')
    for row in rows:
        maxfreq = row[0] + 1.0 
    
    return -math.log(freq/maxfreq)

def information_content_intrinsic (entry):

	#print entry
    rows = connection.execute('''
        SELECT e.desc
        FROM entry e
        WHERE e.id = ?
        ''', (entry,))
    for row in rows:
        freq = row[0] + 1.0
		
    #print (freq)
    rows = connection.execute('''
        SELECT MAX(e.desc)
        FROM entry e
        ''')
    for row in rows:
        maxfreq = row[0] + 1.0 
    
    return -math.log(freq/maxfreq)

def information_content (entry):
    if intrinsic:
        return information_content_intrinsic (entry)
    else: 
        return information_content_extrinsic (entry)

def num_paths (entry1, ancestor):
    
    rows = connection.execute('''
        SELECT COUNT(*)
        FROM transitive t
        WHERE t.entry1=? AND t.entry2=? 
        ''', (entry1, ancestor, ))

    for row in rows:
        npaths = row[0] + 1.0 

    return npaths

def shared_ic_dca (entry1, entry2):

    ancestors = common_ancestors(entry1, entry2)
    dca = {}

    for anc in ancestors:        
        pd = abs(num_paths(entry1, anc) - num_paths(entry2, anc))
        ic = information_content(anc)
        dca[pd] = max(information_content(anc),dca.get(pd,0));
        
    values = dca.values()

    if len(values) > 0 :
        ret = float(sum(values)) / float(len(values))
    else:
        ret = 0

    return ret
    
def shared_ic_mica (entry1, entry2):

    ic = 0 

    ancestors = common_ancestors(entry1, entry2)

    for anc in ancestors:
        ic = max(information_content(anc),ic)

    return ic


def shared_ic (entry1, entry2):
    if mica:
        return shared_ic_mica (entry1, entry2)
    else:
        return shared_ic_dca (entry1, entry2)

def ssm_resnik (entry1, entry2):

    return shared_ic(entry1, entry2)

def ssm_lin (entry1, entry2):

    return 2*shared_ic(entry1, entry2) / (information_content(entry1) + information_content(entry2))

def ssm_jiang_conrath (entry1, entry2):

    distance = information_content(entry1) + information_content(entry2) - 2*shared_ic(entry1, entry2)
    if distance > 0:
        return  1 / distance
    else:
        return 1.0

