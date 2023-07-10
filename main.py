from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
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
def add_contact(name, phone):
    name_field = Name(name)
    record = Record(name_field)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact '{name}' with phone number '{phone}' has been added."


@input_error
def change_phone(name, phone):
    record = address_book.data.get(name)
    if record:
        #old_phone = record.phones[0]
        record.phones[0] = phone
        return f"Phone number for contact '{name}' has been updated to '{phone}'."
    else:
        raise KeyError(f"Contact '{name}' not found.")


@input_error
def get_phone(name):
    record = address_book.data.get(name)
    if record:
        phone_numbers = ", ".join(record.phones)
        return f"The phone number(s) for '{name}' is/are: {phone_numbers}."
    else:
        raise KeyError(f"Contact '{name}' not found.")


def show_all_contacts():
    if not address_book.data:
        return "There are no contacts saved."

    result = ""
    for name, record in address_book.data.items():
        phone_numbers = ", ".join(record.phones)
        result += f"{name}: {phone_numbers}\n"

    return result


def main():
    # print("How can I help you?")
    while True:
        user_input = input(">>>").strip().lower()

        if user_input in ("good bye", "close", "exit"):
            print("Good bye!")
            break

        if user_input == "hello":
            print("How can I help you?")

        elif user_input.startswith("add "):
            data = user_input[4:].split(" ")
            if len(data) != 2:
                print("Give me name and phone please")
            else:
                name, phone = data
                print(add_contact(name, phone))

        elif user_input.startswith("change "):
            data = user_input[7:].split(" ")
            if len(data) != 2:
                print("Give me name and phone please")
            else:
                name, phone = data
                print(change_phone(name, phone))

        elif user_input.startswith("phone "):
            name = user_input[6:].strip()
            print(get_phone(name))

        elif user_input == "show all":
            print(show_all_contacts())

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
