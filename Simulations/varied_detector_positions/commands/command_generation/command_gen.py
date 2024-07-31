# %%
import pandas as pd
import os

# %%
filenames = '../../input/input_generation/filenames.csv'
filenames = pd.read_csv(filenames)
filenames

# %%
sbatch = []
batch = []
for name in filenames['name']:
    with open('template.sh', 'r') as file:
        template = file.read()
        file.close()

    # replace "@filename@" with the filenames
    temp = template
    temp = temp.replace('@name@', name)

    # write the new file
    with open('../'+name+'.sh', 'w') as file:
        file.write(temp)
        file.close()
    
    batch.append('bash commands/'+name+'.sh')
    sbatch.append('sbatch commands/'+name+'.sh')

# write the batch file

check_mctal = True
with open('../../batch.sh', 'w') as file:
    for line in batch:
        # check if file exists
        if check_mctal:
            if not os.path.isfile('../../output/mctal/'+line.split()[1].split('/')[1].split('.')[0]+'.mctal'):
                file.write(line+'\n')
        else:
            file.write(line+'\n')
    file.close()

with open('../../sbatch.sh', 'w') as file:
    for line in sbatch:
        # check if file exists
        if check_mctal:
            if not os.path.isfile('../../output/mctal/'+line.split()[1].split('/')[1].split('.')[0]+'.mctal'):
                file.write(line+'\n')
        else:
            file.write(line+'\n')
    file.close()
