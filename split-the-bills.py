import datetime
import time


class Ledger:
    def __init__(self):
        self.ledger = dict()
        self.exit = False
        self.total = 0
        self.split = 0
        self.command = ["help", "add", "edit", "check", "calculate", "quit", "reset", "export", "main"]

        print("""
            Hei! 
            This program can help you split the bills among friends, i.e. telling who needs to pay extra and by how much.
            All you need to do is adding the name and amount of money that everyone has paid. The program will do the rest.
            Enjoy!
            Hung Nguyen- 28.12.2019
    
            GUIDE:
            
            How to use the program?
            - Input the function commands to activate the function. 
            - To add name and amount of money, first you need to activate the "add" function by typing: 'add' and <Enter>.
            - All names need to be added to split the bills.
            - To see examples at any command, type 'hint'.
            - To calculate the share of everyone: type 'calculate'.
            ***Note: you can switch to another function ANYTIME you want, by simply typing its name. (e.g. 'help' or 'check').""")
        self.help()

    def main(self):
        while True:
            _input = input("Enter function command: ")
            if _input.lower() == "hint":
                print("Example: add")
                print("To check out other available function commands, type 'help'\n")
                break
            if self.check_function_add_or_edit_from_main(_input):
                break
            try:
                eval(class_name + "." + _input.lower() + "()")
            except SyntaxError:
                print("Wrong command, please try again!\n ")
            except AttributeError:
                print("Wrong command, please try again!\n")
            break

    def help(self):
        print(
            """        
            Available function commands:
                add         --- To add name and amount of money paid by the person, can have multiple values. 
                edit        --- To edit name or value that you have input. 
                check       --- To check the all input data.
                calculate   --- To calculate the sum, share of each person, and how much everyone should pay / will get.
                quit        --- To stop and close the program.
                help        --- To see this GUIDE again.
                reset       --- To reset all input data. 
                export      --- To export the results to .txt file
            """)

    def check_and_change_function(self, _input):
        # The following function is to switch to other command function during use if True
        if _input.lower() in self.command:
            eval(class_name + "." + _input.lower() + "()")
            return True
        return False

    def check_and_change_function_split(self, _input):
        # The following function is to switch to other command function during use if True
        if _input[0].lower() in self.command:
            eval(class_name + "." + _input[0].lower() + "()")
            return True
        return False

    def add(self):
        while True:
            _input = input("ADD: Input name and amount: ").split()
            if _input[0].lower() == "hint":
                print("Example: Hung 20 32.95 2.50 OR Hung Eetu Juhani Miikka \n")
                continue
            if _input[0].isdigit():
                print("Looks like you forgot the name. Please enter name and value :)\n")
                continue
            if self.check_and_change_function_split(_input):
                break
            if all(map(lambda k: k.isalpha(), _input)):
                for i in _input:
                    name = i.capitalize()
                    self.ledger.setdefault(name, [])
                print(self.ledger, "\n")
                continue
            try:
                name = _input[0].capitalize()
                value = list(map(float, _input[1:]))
                if any(map(lambda k: k < 0, value)):
                    print("Value of money cannot be negative. Please try again :)")
                    break
                self.ledger.setdefault(name, [])
                self.ledger[name] += value
                print(self.ledger, "\n")
            except ValueError:
                print(
                    "Wrong input, please try again. The correct format is one 'name' and value(s) OR multiple names\n")
                continue

    def edit(self):
        while True:
            _input = input("EDIT: Would you like to remove 'name' or 'value'?: ")
            if _input.lower() == "hint":
                print("Example: name\n")
                continue
            if self.check_and_change_function(_input):
                break
            if not _input.lower() in ["name", "value"]:
                print("Please only enter 'name' or 'value'!")
                continue
            if _input.lower() == "name":
                while True:
                    print("\nEDIT: Here are the names that can be removed:", list(self.ledger.keys()))
                    _input = input("EDIT: Type in name(s) to be removed completely from the list: ")
                    if _input.lower() == "hint":
                        if not self.ledger.keys():
                            print("There is no name to be removed. First add a name")
                        else:
                            print(f"Example: {list(self.ledger.keys())[0]}\n")
                        continue
                    if self.check_and_change_function(_input):
                        break
                    if not all(map(lambda k: k.isalpha(), _input.split())):
                        print("Please only write name(s)!\n ")
                        break
                    try:
                        for i in _input.split():
                            del self.ledger[i.capitalize()]
                        print("Updated: ", self.ledger, "\n")
                        break
                    except KeyError:
                        print("Name(s) not found! please try again. ")
                        print(list(self.ledger.keys()))
            if _input.lower() == "value":
                while True:
                    _input = input(
                        "EDIT: Type in name and value(s) to be removed. "
                        "(To reset values of name(s), enter name(s) and 'reset'): ").split()
                    if _input[0].lower() == "hint":
                        if not self.ledger.keys():
                            print("There is no name to be removed. First add a name and value(s)")
                        else:
                            print(f"Example: {list(self.ledger.keys())[0]}"
                                  f"reset OR {list(self.ledger.keys())[0]} 12.5 \n")
                        continue
                    if self.check_and_change_function_split(_input):
                        break
                    if len(_input) < 2:  # allow multiple reset
                        print("Wrong input! There should be 'name' and value(s) OR 'name' and 'reset'.\n")
                        continue
                    if _input[-1].lower() == "reset":
                        for i in _input[:-1]:
                            foo = dict()
                            foo.setdefault(i.capitalize(), [])
                            self.ledger.update(foo)
                        print("Updated: ", self.ledger, "\n")
                        break
                    try:
                        name = _input[0].capitalize()
                        temp = self.ledger[name]
                        for i in _input[1:]:
                            temp.remove(float(i))
                        print("Updated: ", self.ledger, "\n")
                        break
                    except KeyError:
                        print(
                            "Value/name not found. Please try again. The right input format is 'name' and value(s).\n")
            break

    def check_function_add_or_edit_from_main(self, _input):
        if len(_input.split()) > 1 and _input.split()[0].lower() in ["add", "edit"]:
            command = _input.split()[0].lower()
            info = _input.split()[1:]
            if command == "add":
                if all(map(lambda k: k.isalpha(), info)):
                    for i in info:
                        name = i.capitalize()
                        self.ledger.setdefault(name, [])
                    print(self.ledger)
                    print("Entering function ADD...\n")
                    self.add()
                    return True
                try:
                    name = info[0].capitalize()
                    value = list(map(float, info[1:]))
                    if any(map(lambda k: k < 0, value)):
                        print("Value of money cannot be negative. Please try again :)\n"
                              "Entering function ADD...\n")
                        self.add()
                        return True
                    self.ledger.setdefault(name, [])
                    self.ledger[name] += value
                    print(self.ledger)
                    print("Entering function ADD...\n")
                    self.add()
                    return True
                except ValueError:
                    print("Wrong input, please try again. The correct format is one 'name' and value(s) "
                          "OR multiple names\n Entering function ADD...\n")
                    self.add()
                    return True
            if command == "edit":
                if not info[0] in ["name", "value"]:
                    print("Please write 'name' or 'value'!\n Entering function EDIT...\n")
                    self.edit()
                    return True
                if info[0] == "name":
                    if not all(map(lambda _: _.isalpha(), info[1:])):
                        print("Please write name(s)!\n Entering function EDIT...\n")
                        self.edit()
                        return True
                    try:
                        for i in info[1:]:
                            del self.ledger[i.capitalize()]
                        print("Updated: ", self.ledger)
                        print("Entering function EDIT...\n")
                        self.edit()
                        return True
                    except KeyError:
                        print("Name not found! please try again.\nEntering function EDIT...\n ")
                        self.edit()
                        return True
                if info[0] == "value":
                    if len(info[1:]) < 2:
                        print("Wrong input! There should be 'name' and value(s) "
                              "OR 'name' and 'reset'.\n"
                              "Entering function EDIT...\n")
                        self.edit()
                        return True
                    if info[-1].lower() == "reset":
                        for i in info[1:-1]:
                            foo = dict()
                            foo.setdefault(i.capitalize(), [])
                            self.ledger.update(foo)
                        print("Updated: ", self.ledger, "\n"
                                                        "Entering function EDIT...\n")
                        self.edit()
                        return True
                    try:
                        name = info[1].capitalize()
                        temp = self.ledger[name]
                        for i in info[2:]:
                            temp.remove(float(i))
                        print("Updated: ", self.ledger, "\n"
                                                        "Entering function EDIT...\n")
                        self.edit()
                        return True
                    except KeyError:
                        print("Value/name not found. Please try again. "
                              "The right input format is 'name' and value(s).\n"
                              "Entering function EDIT...\n")
                        self.edit()
                        return True
        return False

    def check(self):
        print("CHECK: ", self.ledger)
        print("")

    def calculate(self):
        while True:
            try:
                temp = list()
                for i in self.ledger.values():
                    temp += i
                self.total = sum(temp)
                self.split = self.total / len(self.ledger.keys())
                print("\nTotal bills:", self.total)
                print("Number of people:", len(self.ledger.keys()))
                print(f"Share of each person: {self.split:.2f}\n")
                for i in self.ledger.keys():
                    difference = sum(self.ledger[i]) - self.split
                    if difference > 0:
                        text = "will"
                        print(f"{i:7} {text:^6} get {difference:.2f}")
                    else:
                        print(f"{i:7} should pay {abs(difference):.2f}")
                print("")
                break
            except ZeroDivisionError:
                print("There is nothing to calculate.\n")
                break

    def quit(self):
        print("\nBye bye! H.")
        print("Closing program...")
        time.sleep(2)
        self.exit = True

    def reset(self):
        self.ledger.clear()
        print("All input data is reset!\n")

    def export(self):
        time = datetime.datetime.now()
        self.calculate()
        with open("Split_bill.txt", "w") as file:
            file.write("----- Split bill program ----- \n")
            file.write(f"Total bills: {self.total} \n")
            file.write(f"Number of people: {len(self.ledger.keys())}\n")
            file.write(f"Share of each person: {self.split:.2f}\n\n")
            for i in self.ledger.keys():
                difference = sum(self.ledger[i]) - self.split
                if difference > 0:
                    text = "will"
                    file.write(f"{i:7} {text:^6} get {difference:.2f}\n")
                else:
                    file.write(f"{i:7} should pay {abs(difference):.2f}\n")
            file.write(f"File created at {time}.")
        print("Export result to Split_bill.txt complete!")


if __name__ == '__main__':
    class_name = "ledger"
    ledger = Ledger()
    while not ledger.exit:
        ledger.main()
