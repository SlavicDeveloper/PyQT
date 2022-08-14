import dis


class ServerCheck(type):
    def __init__(cls, clsname, clsparent, clsdict):
        methods_load_global = []
        methods_load_methods = []
        attrs = []

        for func in clsdict:
            try:
                res = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for el in res:
                    if el.opname == "LOAD_GLOBAL":
                        if el.argval not in methods_load_global:
                            methods_load_global.append(el.argval)
                    elif el.opname == "LOAD_METHOD":
                        if el.argval not in methods_load_methods:
                            methods_load_methods.append(el.argval)
                    elif el.opname == "LOAD_ATTR":
                        if el.argval not in attrs:
                            attrs.append(el.argval)

        if "connect" in methods_load_global:
            raise TypeError("Метод 'connect' не может быть использован в серверном классе")
        if not ("SOCK_STREAM" in attrs and "AF_INET" in attrs):
            raise TypeError("Некорректная инициализация сокета")

        super().__init__(clsname, clsparent, clsdict)


class ClientCheck(type):
    def __init__(cls, clsname, clsparent, clsdict):
        methods_load_global = []
        for func in clsdict:
            try:
                res = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for el in res:
                    if el.opname == "LOAD_GLOBAL":
                        if el.argval not in methods_load_global:
                            methods_load_global.append(el.argval)
        for command in ('accept', 'listen', 'socket'):
            if command in methods_load_global:
                raise TypeError(f"Для данного класса метод {command} запрещен ")
        if "get_message" in methods_load_global or "send_message" in methods_load_global:
            pass
        else:
            raise TypeError("Нет методов 'get message' и 'send message'")
        super().__init__(clsname, clsparent, clsdict)
