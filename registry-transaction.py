# registry-transaction.py  - Program to apply the transaction log(s) to a registry hive.
#
# Copyright (C) 2025 Mark McKinnon (Mark dot McKinnon at Gmail dot com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
# Version History:
#  Initial Version - 1.0 - June 2025
#

from regipy.recovery import apply_transaction_logs
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Apply Registry Transaction Logs to Registry Hive.")
    parser.add_argument("-r", "--registryhive", type=str, action="store",
                        help="Path and name of registry hive")
    parser.add_argument("-p", "--primarytransactionlog", type=str, action="store",
                        help="Path and Name of the Primary Transaction Log")
    parser.add_argument("-s", "--secondarytransactionlog", type=str, action="store",
                        help="Path and Name of the Secondary Transaction Log")
    args = parser.parse_args()

    if args.registryhive is None:
        print ("Path and name of the registry hive was not specified")
        return

    if args.primarytransactionlog is None:
        print ("Path and name of the primary transaction log was not specified")
        return

    if os.path.exists(args.primarytransactionlog):
        primaryTransactionSize = os.path.getsize(args.primarytransactionlog)
        if primaryTransactionSize != 0:
            print(f"Primary Transaction File size: {primaryTransactionSize} bytes")
        else:
            print(f"Primary Transaction File size is 0 bytes, No transactions to process")
            return
    else:
        print(f"Primary Transaction File does not exist: {args.primarytransactionlog}")

    if args.secondarytransactionlog is not None:
        if os.path.exists(args.secondarytransactionlog):
            secondaryTransactionSize = os.path.getsize(args.secondarytransactionlog)
            if secondaryTransactionSize != 0:
                print(f"secondary Transaction File size: {secondaryTransactionSize} bytes")
                secondaryTransactionFile = args.secondarytransactionlog
            else:
                print(f"Secondary Transaction File size is 0 bytes, No secondary transactions to process")
                secondaryTransactionFile = None
        else:
            print(f"Secondary Transaction File does not exist: {args.secondarytransactionlog}")
            print("No secondary transactions to process")
            secondaryTransactionFile = None

    dirtyHive = args.registryhive + "_dirty"
    os.rename(args.registryhive, dirtyHive)

    # Recover hive
    try:
       restoredHivePath, recoverdDirtyPages = apply_transaction_logs(dirtyHive, args.primarytransactionlog, secondaryTransactionFile, args.registryhive)
       os.remove(dirtyHive)
       print(f"Registry Hive {args.registryhive} Recovered successfully")
       print(f"Registry Hive restored to {restoredHivePath}")
       print("Number of recovered dirty pages is " + str(recoverdDirtyPages))
    except:
       print ("Failed to apply transaction logs")
       os.rename(dirtyHive, args.registryhive)

if __name__ == '__main__':
    main()
