import sys
from runMode import defaultMode, staticMode, scrapeMode

# defining the main function
def main():
    args = sys.argv[1:]
    try:
        if len(args) >= 1:
            if args[0] == '--static':
                staticMode.run()
            elif args[0] == '--scrape':
                if len(args) > 1:
                    scrapeMode.run(args[1])     # cmpy1,cmpy2,cmpy3...
                else:
                    scrapeMode.run()
            else:
                defaultMode.run(args[0])    # cmpy1,cmpy2,cmpy3...
        else:
            defaultMode.run()
    except():
        print("Error while retrieving parameters and executing the codebase")


if __name__ == "__main__":
    main()
