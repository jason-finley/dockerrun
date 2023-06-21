from rdkit import Chem
from rdkit.Chem import RDConfig
from rdkit.Chem import Descriptors
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
import os
import sys
sys.path.append(os.path.join(RDConfig.RDContribDir, 'SA_Score'))
import sascorer

import argparse
import json


def compare(first:str, second:str):
    fp1 = FingerprintMols.FingerprintMol(Chem.MolFromSmiles(first))
    fp2 = FingerprintMols.FingerprintMol(Chem.MolFromSmiles(second))

    return str(DataStructs.TanimotoSimilarity(fp1, fp2))


def sascore(first:str):
    mol = Chem.MolFromSmiles(first)
    return sascorer.calculateScore(mol)


def polarea(first:str):
    return Descriptors.TPSA(Chem.MolFromSmiles(first))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-mol", type=str, required=True)
    parser.add_argument("--compare-mol", type=str, required=False)
    parser.add_argument("--fname", type=str, required=False)
    parser.add_argument("--tests", type=str, required=True)
    args = parser.parse_args()

    target_mol = args.target_mol
    compare_mol = args.compare_mol
    fname = args.fname
    tests = args.tests

    output_dict = {}
    tests = list(tests.split(","))

    if tests[0] == "True":
        if compare_mol != "None":
            output_dict["similarity"] = compare(target_mol, compare_mol)
        else:
            output_dict["similarity"] = "Second molecule not inputted"
    if tests[1] == "True":
        output_dict["topological polar surface area"] = polarea(target_mol)
    if tests[2] == "True":
        output_dict["synthetic accessibility score"] = sascore(target_mol)

    print(json.dumps(output_dict, indent=2))

    if fname[-4:] != ".txt":
        fname=fname + ".txt"

    file = open(fname, "w")
    file.write(json.dumps(output_dict, indent=2))
    file.close()
