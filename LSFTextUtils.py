__author__ = 'pascal'


class LSFTextUtils:

    @staticmethod
    def remove_spaces(str):
        result = ''
        for c in str:
            if c != ' ':
                result += c
        return result

    @staticmethod
    def remove_new_line_and_tab(str):
        name = ''
        for c in str:
            if c != '\n' and c != '\t':
                name += c
        return name

    @staticmethod
    def split_string_at_nth_space(str, space):
        space_count = 0
        char_count = 0
        result = ('','')
        for c in str:
            char_count += 1
            if c == ' ':
                space_count += 1
            if space_count == space and char_count < len(str):
                result = (str[:char_count], str[char_count:])
                break
        return result

    @staticmethod
    def correct_time_string(str):
        hour = int(str[:2])
        if hour > 23:
            hour = hour - 24
            str = unicode(hour) + u':' + str[3:]
        return str

    @staticmethod
    def split_string_at_last_space(str):
        space_position = 0
        char_count = 0
        for c in str:
            if c == ' ':
                space_position = char_count
            char_count += 1
        return (str[:space_position], str[space_position+1:])

    @staticmethod
    def remove_spaces_at_beginning(str):
        result = ''
        aux = False
        for c in str:
            if c != ' ' or aux is True:
                result += c
                aux = True
        return result

    @staticmethod
    def remove_spaces_at_end(str):
        result = ''
        idx = 0
        last_space = 0
        aux = False
        for c in str:
            if c == ' ':
                if aux == False:
                    last_space = idx
                    aux = True
            else:
                aux = False
            idx += 1
        result = str[0:last_space]
        return result

    @staticmethod
    def rename_TGS(str):
        result = ''
        if str[0:11] == 'Technologie':
            result = 'TGS ' + str[42:]
        else:
            result = str
        return result





