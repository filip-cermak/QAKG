import os

os.system("rm -rf output/classified")
os.system("rm -rf output/classified")
os.system("rm -rf output/output")
os.system("rm -rf result")

for file in os.listdir("output/data/OIE_2016"):
    if file != "P0.jsonl":
        os.remove("output/data/OIE_2016/" + file)
