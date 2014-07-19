from bin import cli_browser


def main():
    repository = raw_input("Offer a package name: ")
    cmd_browser = cli_browser.cli_browser()
    cmd_browser.setRequestedURL("https://github.com/search?q={0}&type=Repositories&ref=searchresults".format(repository))
    response = cmd_browser.submit()
    repos_list = cmd_browser.parseResponse(response)

    length = len(repos_list)
    for repo_index in range(length):
        print "[{0:2}] : {1}".format((repo_index+1), repos_list[repo_index][1:])

    print "Current page: {0}".format(cmd_browser.getCurrentPage())
    print "Available pages: ",
    pages = cmd_browser.parsePagination(response)
    for page in pages[:]:
        print("{0:1}".format(page)),

if __name__ == "__main__":
    import sys
    print sys.argv
    main()