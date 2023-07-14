from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Field:
    def __init__(self, value=None):
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

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError("Phone number not found.")


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
    name = args[0]
    phone = args[1]
    name_field = Name(name)
    record = Record(name_field)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact '{name}' with phone number '{phone}' has been added."


@input_error
def change_phone(*args):
    name = args[0]
    phone = args[1]
    record = address_book.data.get(name)
    if record:
        # old_phone = record.phones[0]
        record.phones[0] = phone
        return f"Phone number for contact '{name}' has been updated to '{phone}'."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def get_phone(*args):
    name = args[0]
    record = address_book.data.get(name)
    if record:
        phone_numbers = ", ".join(record.phones)
        return f"The phone number(s) for '{name}' is/are: {phone_numbers}."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def show_all_contacts(*args):
    if not address_book.data:
        return "There are no contacts saved."

    result = ""
    for name, record in address_book.data.items():
        phone_numbers = ", ".join(record.phones)
        result += f"{name}: {phone_numbers}\n"

    return result


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
    
