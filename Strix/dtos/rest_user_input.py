from dataclasses import dataclass


@dataclass
class RestUserInput:
    first_name: str
    last_name: str
    password: str
    email: str