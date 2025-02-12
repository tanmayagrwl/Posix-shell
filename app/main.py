import sys
import shutil
import os
import shlex


def main():
    builtins = ["echo", "exit", "type", "pwd", "cd"]

    while True:
        sys.stdout.write("$ ")
        userInputCommand = input().strip()
        if userInputCommand == "":
            continue
        parts = shlex.split(userInputCommand)
        shellCommand = parts[0]
        

        # FOR ECHO
        if shellCommand == "echo":
            print(" ".join(shlex.split(userInputCommand[5:])))
            
        # FOR EXIT
        elif userInputCommand == "exit 0":
            sys.exit(0)
        # FOR TYPE
        elif shellCommand == "type":
            if len(parts) < 2:
                print("type: missing operand")
                continue

            targetCommand = parts[1]

            if targetCommand in builtins:
                print(f"{targetCommand} is a shell builtin")
            elif path := shutil.which(targetCommand):
                print(f"{targetCommand} is {path}")
            else:
                print(f"{targetCommand}: not found")
        # FOR PWD
        elif shellCommand == "pwd":
            print(os.getcwd())

        # FOR CD
        elif shellCommand == "cd":
            if len(parts) < 2 or parts[1] == "~":
                home = os.path.expanduser("~")
                os.chdir(home)
                continue

            path = parts[1]

            if not os.path.exists(path):
                print(f"cd: {path}: No such file or directory")
                continue

            if not os.path.isdir(path):
                print(f"cd: {path}: Not a directory")
                continue

            try:
                if path.startswith("~"):
                    absolute = os.path.expanduser(path)
                elif path.startswith("/"):
                    absolute = path
                elif path.startswith("."):
                    absolute = os.path.join(os.getcwd(), path)
                    absolute = os.path.normpath(absolute)
                else:
                    absolute = None
                    print(f"{path}: unsupported path")
                    continue

                os.chdir(absolute)
            except Exception as e:
                print(f"cd: {e}")

        # FOR CAT COMMAND
        elif shellCommand == "cat":
            if len(parts) < 2:
                print("cat: missing operand")
                continue

            for file in parts[1:]:
                # Use os.path.realpath to resolve the full path
                targetFile = os.path.realpath(file)

                if not os.path.exists(targetFile):
                    print(f"cat: {repr(file)}: No such file or directory")
                    continue

                if not os.path.isfile(targetFile):
                    print(f"cat: {repr(file)}: Is a directory")
                    continue

                try:
                    with open(targetFile, "r") as f:
                        sys.stdout.write(f.read())
                except Exception as e:
                    print(f"cat: {e}")
            sys.stdout.write("\n")

            
        # FOR INVALID COMMAND
        else:
            print(f"{userInputCommand}: command not found")


        


if __name__ == "__main__":
    main()
