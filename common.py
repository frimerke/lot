#
# Universal Functions
#
def filter_nonprintable(text):
    import string
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})

def dir_handling(title, cwd):
    import os
    try:
        workingdir = cwd + title.strip()
        os.mkdir(workingdir)
    except:
        workingdir = cwd + title.strip() + "1"
        os.mkdir(workingdir)
    os.chdir(workingdir)
    return workingdir

def download(url, filename, minmax):
    import requests
    try:
        r = requests.get(url)
        with open(filename, "wb") as code:
            code.write(r.content)
    except:
        pass
