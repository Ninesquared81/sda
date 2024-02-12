import argparse
import dataclasses
import enum


class TokenType(enum.StrEnum):
    STRING = "string"
    NUMBER = "number"
    PD = "pd"
    MAD = "mad"


@dataclasses.dataclass
class Token:
    type: TokenType
    value: str | int

    def __iter__(self):
        return iter(dataclasses.astuple(self))


class Opcode(enum.Enum):
    PD = enum.auto()
    MAD = enum.auto()
    STRING = enum.auto()
    NUMBER = enum.auto()


@dataclasses.dataclass
class Op:
    opcode: Opcode
    args: tuple

    def __iter__(self):
        return iter(dataclasses.astuple(self))


def lex(source_code: str) -> list[Token]:
    tokens = []
    i = 0
    while i < len(source_code):
        while source_code[i].isspace():
            i += 1
            if i >= len(source_code):
                return tokens
        if source_code[i] == '"':
            # string
            i += 1  # Consume opening '"'.
            start = i
            while i < len(source_code) and source_code[i] != '"':
                i += 1
            value = source_code[start:i]
            tokens.append(Token(type=TokenType.STRING, value=value))
            i += 1  # Consume closing '"'.
        elif source_code[i].isdigit():
            # number
            start = i
            while i < len(source_code) and source_code[i].isdigit():
                i += 1
            value = source_code[start:i]
            tokens.append(Token(type=TokenType.NUMBER, value=int(value)))
        else:
            start = i
            while i < len(source_code) and source_code[i].isalpha():
                i += 1
            value = source_code[start:i]
            match value:
                case "mad":
                    token_type = TokenType.MAD
                case "pd":
                    token_type = TokenType.PD
                case _:
                    raise ValueError(f"Unknown token {value!r}")
            tokens.append(Token(type=token_type, value=value))
    return tokens


def parse(tokens: list[Token]) -> list[Op]:
    ops = []
    i = 0
    while i < len(tokens):
        token_type, value = tokens[i]
        match token_type:
            case TokenType.MAD:
                ops.append(Op(Opcode.MAD, ()))
            case TokenType.PD:
                ops.append(Op(Opcode.PD, ()))
            case TokenType.STRING:
                ops.append(Op(Opcode.STRING, (value,)))
            case TokenType.NUMBER:
                ops.append(Op(Opcode.NUMBER, (value,)))
        i += 1
    return ops


def interpret(ops: list[Op]) -> None:
    d = bytearray()
    a: list[int] = []
    for op in ops:
        match op:
            case Op(Opcode.MAD, _):
                d.append(a.pop())
            case Op(Opcode.PD, _):
                print(d.decode())
            case Op(Opcode.STRING, (string,)):
                d.extend(string.encode())
            case Op(Opcode.NUMBER, (number,)):
                a.append(number)


def main() -> None:
    argparser = argparse.ArgumentParser(description="Interpret an SDA file")
    argparser.add_argument("filename")
    args = argparser.parse_args()
    with open(args.filename) as f:
        source_code = f.read()
    tokens = lex(source_code)
    print(tokens)
    ops = parse(tokens)
    print(ops)
    interpret(ops)


if __name__ == "__main__":
    main()
