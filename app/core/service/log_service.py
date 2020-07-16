def get_log_string(file_name):
    """
        get full log string
    :param file_name: log file path
    :return: full log string
    """
    with open(file_name) as file_obj:
        content = file_obj.read()
        return content


def get_log_file_length(file_name):
    """
        get length of log file
    :param file_name: log file path
    :return: length of log file
    """
    count = 0
    for index, line in enumerate(open(file_name, 'r')):
        count += 1
    return count


def get_line(the_file_path, line_number):
    """
        get log of specific line
    :param the_file_path: log file path
    :param line_number: line number
    :return: log string
    """
    line_number = int(line_number)
    if line_number < 1:
        return ''
    for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
        if cur_line_number == line_number - 1:
            return line
    return ''


def get_new_log(the_file_path, last_unread_line):
    """
        get log of specific line
    :param last_unread_line: last unread line
    :param the_file_path: log file path
    :return: log string
    """
    log = ''
    line_number = int(last_unread_line)
    if line_number < 1:
        return ''
    for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
        if cur_line_number >= line_number - 1:
            log = log + line
    return log
