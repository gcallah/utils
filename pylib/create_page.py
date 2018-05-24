indent1 = "            " # type: str
indent2 = "                    " # type: str

def create_page(inf, outf, page_nm):
    for line in inf:
        outf.write(line)
        if "<title>" in line:
            outf.write(indent1 + page_nm + "\n")
        if "<h1>" in line:
            outf.write(indent2 + page_nm + "\n")
