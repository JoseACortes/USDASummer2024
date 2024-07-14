# %%
import pandas as pd
import os

# %%
filenames = '../../input/input_generation/filenames.csv'
filenames = pd.read_csv(filenames)
filenames

# %%
sbatch = []
for name in filenames['name']:
    with open('local_template.sh', 'r') as file:
        template = file.read()
        file.close()

    # replace "@filename@" with the filenames
    temp = template
    temp = temp.replace('@name@', name)

    # write the new file
    with open('../local-'+name+'.sh', 'w') as file:
        file.write(temp)
        file.close()

    sbatch.append('bash commands/local-'+name+'.sh')

# write the sbatch file


check_mctal = True
with open('../../local_batch.sh', 'w') as file:
    for line in sbatch:
        # check if file exists
        if check_mctal:
            if not os.path.isfile('../../output/mctal/'+line.split()[1].split('/')[1].split('.')[0]+'.mctal'):
                file.write(line+'\n')
        else:
            file.write(line+'\n')
    file.close()


