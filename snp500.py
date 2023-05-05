import sys
from datetime import datetime

from runMode import defaultMode, staticMode, scrapeMode


# defining the main function for S&P 500 project
def main():
    start_time = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        args = sys.argv[1:]     # selecting parameters after the execution file name
        if len(args) >= 1:     # if number of parameters > 1
            if args[0] == '--static':     # checking if the 2nd param is static
                print("------------ STATIC MODE ------------")
                staticMode.run()     # executing the static flow
            elif args[0] == '--scrape':     # checking if the 2nd parameter is scrape
                print("------------ SCRAPE MODE ------------")
                if len(args) > 1:     # if it has more parameters executing scrape flow with cmpy dtls
                    scrapeMode.run(args[1])     # cmpy1,cmpy2,cmpy3...
                else:
                    scrapeMode.run()     # executing the scrape flow
            else:     # else executing default flow
                print("------------ DEFAULT MODE ------------")
                defaultMode.run(args[0])    # cmpy1,cmpy2,cmpy3...
        else:
            print("------------ DEFAULT MODE ------------")
            defaultMode.run()     # else executing default flow
        end_time = datetime.now().strftime("%Y%m%d%H%M%S")
        print("Total Execution Time : ", (int(end_time)-int(start_time)), " secs")
    except():
        print("Error while retrieving parameters and executing the codebase")     # command to print if any exceptions occur in the codebase


if __name__ == "__main__":     # start of the module
    main()     # calling the main function
