import os
import argparse

def all_to_years(min_year, max_year):
    with open("putnam.lean", "r") as f:
        lines = f.readlines()
        for year in range(max_year, min_year - 1, -1):
            filename = f"putnam_{year}.lean"
            with open(filename, "w") as g:
                g.write("import Mathlib\nopen BigOperators\n\n")
                is_in_section = False
                for line in lines:
                    if is_in_section:
                        if line.strip() == f"end putnam_{year}":
                            break
                        g.write(line)
                    elif line.strip() == f"section putnam_{year}":
                        is_in_section = True

def years_to_all(min_year, max_year):
    with open("putnam_all.lean", "w") as f:
        f.write("import Mathlib\nopen BigOperators\n\n")
        for year in range(min_year, max_year + 1):
            filename = f"putnam_{year}.lean"
            with open(filename, "r") as g:
                lines = g.readlines()
                f.write(f"section putnam_{year}\n")
                for line in lines:
                    if line.strip() == "import Mathlib" or line.strip() == "open BigOperators":
                        continue
                    f.write(line)
                f.write(f"end putnam_{year}\n")

def all_to_individual(min_year, max_year):
    return
    # first read the entire file, and proceed line by line
    # keep track of the content in blocks seperated by empty lines, and keep track of the namespaces opened with "open {NAMESPACE}" in the current "section"
    # for each block, create a new file with the content of the block, the relevant namespaces opened, and the name of the file is the name of the problem in the block : "putnam_{year}_{number}"
    with open("putnam.lean", "r") as f:
        lines = f.readlines()
        is_in_section = False
        section_name = ""
        section_opens = []
        for line in lines:
            if is_in_section:
                if line.strip() == f"end {section_name}":
                    # get the file name from the collected content

                    filename = f"putnam_{section_name}.lean"
                    with open(filename, "w") as g:
                        g.write("import Mathlib\nopen BigOperators\n")
                        for namespace in namespaces:
                            g.write(f"open {namespace}\n")
                        g.write("\n")
                        for line in section_content:
                            g.write(line)
                    is_in_section = False
                    section_name = ""
                    section_content = []
                    namespaces = set()
                else:
                    section_content.append(line)
                    if "open" in line:
                        namespaces.add(line.strip().split(" ")[1])
            elif line.strip().startswith("section putnam_"):
                is_in_section = True
                section_name = line.strip().split(" ")[1]


if __name__ == '__main__':
    # make an argument parser which takes in the min and max year, and the type of conversion desired (either all_to_years, years_to_all)
    # this will be called from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("min_year", type=int)
    parser.add_argument("max_year", type=int)
    parser.add_argument("start_format", type=str, choices=["all", "years"])
    parser.add_argument("end_format", type=str, choices=["all", "years"])
    args = parser.parse_args()
    if args.start_format == "all" and args.end_format == "years":
        all_to_years(args.min_year, args.max_year)
    else:
        raise ValueError("Invalid conversion format")
