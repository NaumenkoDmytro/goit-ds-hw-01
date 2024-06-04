from models import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except KeyError as e:
            return f"KeyError: {e}"
        except IndexError as e:
            return f"IndexError: {e}"

    return inner


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:  # check if we have all arguments to work with from the list
        raise ValueError("Please enter the Name and birthday date")
    name, date = args
    record: Record = book.find(name)
    if record is None:
        return "Sorry no User found"
    else:
        record.add_birthday(date)
        return "The birthday date was added"


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:  # check if we have all arguments to work with from the list
        raise ValueError("Please enter the Name")
    name = args[0]  # we do it to ge a string not list :)
    record: Record = book.find(name)
    if record is None or record.birthday is None:
        return "Sorry no data about this user's birthday date"
    else:
        return record.birthday.value


@input_error
def birthdays(book: AddressBook):
    birthday_list = [str(record) for record in book.get_upcoming_birthdays()]
    return "\n".join(birthday_list) if birthday_list else "No data available"


@input_error
# Function that show all contacts.
def show_all(book: AddressBook):
    records = [str(record) for record in book.values()]
    records_string = "\n".join(records)
    return records_string if records else "No data available"


@input_error
# Function that show Phone number by users name.
def show_phone(args, book: AddressBook):
    if args:
        name = args[0]
        record: Record = book.find(name)
        if record:  # Check if we have this contact in the dictionary
            return book.find(name)
        else:
            raise KeyError(
                "This contacts is not exist, use 'add' command to create a new one"
            )
    else:
        return f"User name was not provided"


@input_error
# Function that change a phone number by users name.
def change_contact(args, book: AddressBook):
    if len(args) < 3:  # check if we have all arguments to work with from the list
        raise ValueError(
            "To change the contact you need to provide name that exist in phonebook and a new phone"
        )
    name, old_phone, new_phone = args
    record: Record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact updated."


@input_error
def parse_input(user_input):
    user_input = user_input.strip()
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:  # check if we have all arguments to work with from the list
        raise ValueError(
            "To add the number you need to provide a name and a personal phone"
        )
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    if phone in [phone.value for phone in record.phones]:
        return "The number is already exist"
    record.add_phone(phone)
    return "Contact added."
