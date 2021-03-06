import require_utils
import pdb
import lan
import sender
import generator
import report as generate_report
from os.path import basename

'''
DRAFT:
 - Need to sort project
 - Config from file
 - Globals from repo
 - Forming globals
 - Fix bug with empty repos
'''
def main(gerritAccount, mode_on, type_req_on, branch_name_on, global_branch, send_on=False, e_mail=''):
    try:
        #pdb.set_trace()
        pack_count = (0, 0)
        file_extension = ''
        type_req = type_req_on

        if type_req not in ["spec", "control"]:
            type_req = ''

        branch_name = branch_name_on
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'

        while file_extension.lower() not in ['pdf', 'html']:
            file_extension = raw_input('With what extension save a file? (PDF or HTML?) ')

        '''while send.lower() not in ['y', 'n', 'yes', 'no']:
            send = raw_input('Would you like to send a report on whether the e-mail? ')
            if send.lower() in ['y', 'yes']:
                email = raw_input('Enter the e-mail: ')
            elif send.lower() in ['n', 'no']:
                pass'''
        '''if send_on:
            email = raw_input('Enter the e-mail: ')
        else:
            pass'''

        json_file = open('requirements.json', 'w')
        generate_report.generate_header(json_file, branch)

        mode = str(mode_on)

        if mode == 'requirements':
            req_url = 'https://raw.githubusercontent.com/openstack/requirements/{0}/global-requirements.txt'.format(global_branch)
            r = lan.get_requirements_from_url(req_url, gerritAccount)
            rq2 = require_utils.Require(require_utils.Require.parse_req(r))
        else:
            json_file.write('\t{\n')

        try:
            f = open('repos_name', 'r')
        except IOError:
            file_exist_check = True
            while file_exist_check:
                repo_file = raw_input('Enter the file with repos name: ')
                try:
                    with open(basename(repo_file), 'r') as req_file:
                        if mode == 'requirements':
                            pack_count = generator.get_req(gerritAccount, req_file, rq2, json_file, branch, type_req)
                            file_exist_check = False
                        else:
                            generator.get_epoch(gerritAccount, req_file, branch, json_file)
                            file_exist_check = False
                except IOError:
                    print 'No such file or directory'

        if mode == 'epoch':
            json_file.write('\n' + '\t' * 2 + '}' + '\n')
        json_file.write('\t' + '],\n"output_format": "' + file_extension.lower() + '"\n}')
        json_file.close()

        generate_report.generate_output(mode)

        if send_on:
            text = str(pack_count[0]) + ' packages were changed in ' + str(pack_count[1]) + ' repos.'
            sender.send_mail(e_mail, 'Report from ' + sender.cur_time, text, 'report.' + file_extension.lower())
        else:
            raise SystemExit
    except KeyboardInterrupt:
        print 'The process was interrupted by the user'
        raise SystemExit