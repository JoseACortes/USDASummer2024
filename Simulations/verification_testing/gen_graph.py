import INS_Analysis as insd
import argparse

parser = argparse.ArgumentParser(description='Generate a graph for the given name.')
parser.add_argument('name', type=str, help='Name of the output file without extension')
args = parser.parse_args()

# Step 5: Use the name argument
name = args.name
filename = 'output/mctal/'+name+'.mctal'

bins, vals = insd.read(filename, tally=58, start_time_bin=0, end_time_bin=1, nps=1e6)

# plot the data
import matplotlib.pyplot as plt
for _, vals in enumerate(vals):
    plt.plot(bins, vals, label=str(_))
plt.xlabel('Energy (MeV)')
plt.ylabel('Counts')
plt.title(name)

plt.legend()
# plt.xlim(4, 5)
# plt.ylim(0, 25)

# save the data
plt.savefig('output/graph/'+name+'.png')