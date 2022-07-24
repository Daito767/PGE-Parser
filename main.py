import ParserJumpPGE
from ColoredText import *
import GoogleSpreadSheet
import colorama
import local_config as config


class Program:
    def __init__(self):
        colorama.init()

        print_blue('[INFO]')
        print(' The program was written by Ioan')

        self.parser = ParserJumpPGE.ParserJumpPGE()
        self.sheet_api = GoogleSpreadSheet.SpreadSheetAPI()

        self.pge_email = ''
        self.pge_password = ''

        self.sheet_id = ''

    def run(self):
        print_blue('[INPUT]')
        action = input(' Enter the action you need (populate, check): ')

        while action not in ('populate', 'check'):
            print_yellow('[WARNING]')
            print(' Insert a valid value option: populate, check')

            print_blue('[INPUT]')
            action = input(' Enter the action you need (populate, check): ')

        if not self.sheet_api.try_to_authorize():
            return

        if not self.pge_try_to_login():
            return

        print_blue('[INPUT]')
        self.sheet_id = input(' Enter the table id: ')

        if action == 'populate':
            self.run_pole_data_fill()
        elif action == 'check':
            pass
        else:
            return

    def pge_try_to_login(self) -> bool:
        print_blue('[INPUT]')
        use_default_login_data = input(' Use default pge login data (y, n, cancel): ')

        while use_default_login_data not in ('y', 'n', 'cancel'):
            print_yellow('[WARNING]')
            print(' Insert a valid value option: y, n, cancel')

            print_blue('[INPUT]')
            use_default_login_data = input(' Use default pge login data (y, n, cancel): ')

        if use_default_login_data == 'y':
            self.pge_email = config.pge_email
            self.pge_password = config.pge_password
        elif use_default_login_data == 'n':  #TODO: Fa ca utilizatorul sinfur sa se autentifice
            print_blue('[INPUT]')
            self.pge_email = input(' Enter the email from pge account: ')

            print_blue('[INPUT]')
            self.pge_password = input(' Enter the password from pge account: ')
        else:
            exit()

        return self.parser.user_login(self.pge_email, self.pge_password)

    def run_pole_data_fill(self):
        print_yellow('[INFO]')
        print(' Data filling has started')

        needed_data = self.sheet_api.identify_necessary_data(self.sheet_id)

        results = {}

        n = 1
        for sap_id in needed_data[1]:
            if sap_id in results.keys():
                print_red('[ERROR]')
                print(f' Multiple poles with the same "{sap_id}"')

            if not sap_id.isnumeric():
                n += 1

            general_data = self.parser.collect_general_pole_data(sap_id)
            inspection_data = self.parser.collect_inspection_pole_data(sap_id)
            results[sap_id] = [general_data, inspection_data]

            self.sheet_api.populate_pole(self.sheet_id, f'C{n + 1}:S{n + 1}', general_data, inspection_data, needed_data[0])

            n += 1


if __name__ == '__main__':
    program = Program()
    program.run()

