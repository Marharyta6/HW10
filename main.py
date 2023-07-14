from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return wrapper


address_book = AddressBook()


@input_error
def add_contact(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def get_phone(*args):
    name = Name(args[0])
    #record = Record(name)
    rec: Record = address_book.get(str(name))
    if rec:
        return f"The phone number(s) for '{name}' is/are: {', '.join(str(p) for p in rec.phones)}."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def show_all_contacts(*args):
    return address_book
    # if not address_book.data:
    #     return "There are no contacts saved."

    # result = ""
    # for name, record in address_book.data.items():
    #     phone_numbers = ", ".join(record.phones)
    #     result += f"{name}: {phone_numbers}\n"

    #return result


def greeting_command(*args):
    return "How can I help you?"


def exit_command(*args):
    return "Good bye!"


def unknown_command(*args):
    return "Invalid command. Please try again."


COMMANDS = {add_contact: ("add", ),
            change_phone: ("change",),
            get_phone: ("phone",),
            show_all_contacts: ("show all", ),
            greeting_command: ("hello", ),
            exit_command: ("good bye", "close", "exit")
            }


def parser(user_input):
    for command, kwds in COMMANDS.items():
        for kwd in kwds:
            if user_input.lower().startswith(kwds):
                return command, user_input[len(kwd):].strip().split()
    return unknown_command, []


def main():
    # print("How can I help you?")
    while True:
        user_input = input(">>>")

        func, data = parser(user_input)

        print(func(*data))

        if func == exit_command:
            break


if __name__ == "__main__":
    main()
    
