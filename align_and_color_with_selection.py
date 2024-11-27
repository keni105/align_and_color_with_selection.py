from pymol import cmd, util
import os

# Function to align two structures, color-code differing residues, and create selections
def align_and_color_with_selection(struct1, struct2):
    """
    Align two structures, color code differing residues, and create selections for them.

    :param struct1: Name of the first structure (e.g., model1)
    :param struct2: Name of the second structure (e.g., model2)
    """
    # Align the structures
    alignment_result = cmd.align(struct1, struct2)
    print(f"Alignment RMSD: {alignment_result[0]}")

    # Fetch sequences for comparison
    seq1 = cmd.get_fastastr(struct1).splitlines()[1:]
    seq2 = cmd.get_fastastr(struct2).splitlines()[1:]

    seq1 = ''.join(seq1)
    seq2 = ''.join(seq2)

    # Check if sequences are the same length
    if len(seq1) != len(seq2):
        print("Warning: Sequence lengths are different. Alignment might be imperfect.")

    differing_residues_1 = []
    differing_residues_2 = []

    # Color residues by difference and collect differing residues
    for i, (res1, res2) in enumerate(zip(seq1, seq2), start=1):
        selection1 = f"{struct1} and resi {i}"
        selection2 = f"{struct2} and resi {i}"
        
        if res1 != res2:
            cmd.color("red", selection1)
            cmd.color("red", selection2)
            differing_residues_1.append(i)
            differing_residues_2.append(i)
        else:
            cmd.color("green", selection1)
            cmd.color("green", selection2)

    # Create selections for differing residues
    if differing_residues_1:
        diff_selection1 = f"{struct1}_diff_residues"
        diff_selection2 = f"{struct2}_diff_residues"
        
        cmd.select(diff_selection1, f"{struct1} and resi {'+'.join(map(str, differing_residues_1))}")
        cmd.select(diff_selection2, f"{struct2} and resi {'+'.join(map(str, differing_residues_2))}")
        
        print(f"Differing residues selection created: {diff_selection1} and {diff_selection2}")
    else:
        print("No differing residues found.")

# Add command to PyMOL
cmd.extend("align_and_color_with_selection", align_and_color_with_selection)

# Plugin Interface
def __init_plugin__(self=None):
    from pymol.plugins import addmenuitem
    addmenuitem("Align, Color, and Select Differences", lambda s=cmd: align_and_color_with_selection())
