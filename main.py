#
#   -------------------------------------------------------------------------------------------------
#   |   Alunos :                                                                                    |
#   |                                                                                               |
#   |       - Júlio Cesar Roque da Silva                                                            |
#   |       - José Gustavo de Oliveira Cunha                                                        |
#   |       - José Thiago Torres da Silva                                                           |
#   |       - João Victor Mendes de Lira                                                            |
#   |       - Gabriel Valdomiro da Silva                                                           |
#   -------------------------------------------------------------------------------------------------
#

# Libraries Imports
import re
import os
import sys
import time

# Tools
date_2021_regex = re.compile(r"[0-9]{2}/[A-Z][a-z]{2}/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}")
http_success_status_regex = re.compile(r"2\d\d [0-9]{1,9}")


# Auxiliary Functions
def input_validate(input_value: int) -> int:
    condition = True
    while condition:
        valid_inputs = [0,1,2,3,4]
        if input_value.isnumeric() and (eval(input_value) in valid_inputs):
            return eval(input_value)
        else:
            input_value = input("Digite um valor válido: ")


def create_dir() -> None:
    try:
        if "./Análise":
            os.makedirs("./Análise")
    except OSError:
        ...


def write_to_file(file_name: str, content: list, op: str) -> None:
    create_dir()
    with open(file_name, op) as file:
        file.writelines(content)


def clean() -> None:
    platform = sys.platform
    if platform == 'win32':
        os.system('cls')
    elif platform == 'linux' or platform == 'linux2':
        os.system('clear')


def show_time(initial_time: float) -> None:
    print(f"Tempo de Execução da ultima requisição {time.time() - initial_time:.2f}\n")


# Save a .txt archive with a http code from the response, the length of the response and the address of the request
def big_requests_answered() -> None:
    initial_time = time.time()
    print("Executando...")

    ip_regex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    response = []

    access_log = open("access.log", "r")

    for request in access_log:
        http_success_status_regex_ok = http_success_status_regex.findall(request)

        if http_success_status_regex.findall(request) and eval(http_success_status_regex_ok[0][3::]) > 2000:
            ip_data = ip_regex.findall(request)

            response.append(http_success_status_regex_ok[0] + " " + ip_data[0] + '\n')

    write_to_file('./Análise/recursosGrandes.txt', response, 'w+')
    clean()
    show_time(initial_time)
    access_log.close()


# Save a .txt archive with a http code, the address of the requested, month and year of the request
def not_answered_requests() -> None:
    initial_time = time.time()
    print("Executando...")

    regex_bad_request = re.compile(r" 4[0-9]{2} ")
    regex_date = re.compile(r"[0-9]{2}/Nov/2021:[0-9]{2}:[0-9]{2}:[0-9]{2} [+][0-9]{4}")
    regex_address = re.compile(r"(\"http[s]?://)(.*?)(\")")
    response = []

    access_log = open("access.log", "r")

    for request in access_log:
        http_bad_request = regex_bad_request.findall(request)
        request_date = regex_date.findall(request)

        if http_bad_request and request_date:
            request_address = regex_address.findall(request)

            if request_address:
                address = "".join(request_address[0])
                if (address != ""):
                    response.append(
                            http_bad_request[0].strip() + " " + address + " " + request_date[0] + "\n"
                    )

    
    write_to_file("./Análise/nãoRespondidosNovembro.txt", response, "w+")
    clean()
    show_time(initial_time)
    access_log.close()


# Create a .txt with the percentage of requests by SO, in the year 2021
def requests_by_operational_system() -> None:

    initial_time = time.time()
    print("Executando...")

    def take_operational_system_percentage(operational_system_quantitative: dict) -> float:
        number_of_requests = sum(1 for line in open("access.log")) 
        percentage = (operational_system_quantitative / number_of_requests) * 100
        return percentage

    access_log = open("access.log", "r")

    operational_systems = {
        "Windows": 0,
        "Linux": 0,
        "Macintosh": 0,
    }

    sub_linux_x11 = {
        "Ubuntu": 0,
        "Fedora": 0,
    }

    sub_linux_mobile = {
        "Mobile": 0
    }

    sub_linux_others = {
        "Linux and others": 0
    }

    def sub_linux_validator(request: str) -> None:
        if ((re.compile(r'X11').findall(request))):
            for sub_system in sub_linux_x11:
                if (sub_system in request):
                    sub_linux_x11[sub_system] += 1
                else:
                    sub_linux_others["Linux and others"] += 1
        elif (re.compile(fr"{system}; Android").findall(request) or re.compile(r";Mobile;").findall(request)):
            sub_linux_mobile["Mobile"] += 1
    

    for request in access_log:
        if (re.findall(date_2021_regex, request)):
            for system in operational_systems:
                if (system == "Linux"):
                    sub_linux_validator(request)
                else:
                    if (re.findall(fr"{system}", request)):
                        operational_systems[system] += 1

    table_of_percent = {

        "Windows": operational_systems["Windows"],
        "Macintosh": operational_systems["Macintosh"],
        "Ubuntu": sub_linux_x11["Ubuntu"],
        "Fedora": sub_linux_x11["Fedora"],
        "Mobile": sub_linux_mobile["Mobile"],
        "Linux, outros": sub_linux_others["Linux and others"]
    }

    response = ""

    for line_content in table_of_percent:
        response += (f'{line_content} {take_operational_system_percentage(table_of_percent[line_content])}\n')

    clean()
    show_time(initial_time)
    write_to_file("./Análise/requestsPorSistemaOperacional.txt", response, "w+")
    access_log.close()


# Print in the console the average of success POST requests from the year 2021
def average_requests_post() -> None:
    initial_time = time.time()
    print("Executando...")
    access_log = open("./access.log", "r")

    req_post_regex = re.compile(r"POST")

    total_post_requests_with_success = 0
    sum_of_all_post_requests_with_success_length = 0

    for request in access_log:
        http_status_data = http_success_status_regex.findall(request)
        if re.findall(date_2021_regex, request) and req_post_regex.findall(request) and http_status_data:
            total_post_requests_with_success += 1
            http_status, request_size = http_status_data[0].split()
            sum_of_all_post_requests_with_success_length += int(request_size)
    clean()
    show_time(initial_time)
    access_log.close()
    average_of_all_post_requests_with_success = sum_of_all_post_requests_with_success_length / total_post_requests_with_success
    print(f"Média das requisições POST de 2021 respondidas com sucesso: {average_of_all_post_requests_with_success:.4f}")


# Main function
def menu() -> None:

    execution_condition = True
    while execution_condition:
        menu_option = input_validate(input(
"""
1 - Recursos grandes respondidos
2 - Não respondidos
3 - "%" de requisições por SO
4 - Média das requisições POST
0 - Sair\n
Digite a opção desejada: """))

        match menu_option:
            case 1:
                big_requests_answered()
            case 2:
                not_answered_requests()
            case 3:
                requests_by_operational_system()
            case 4:
                average_requests_post()
            case 0:
                execution_condition = False

# Principal archive
if __name__ == '__main__':
    menu()
