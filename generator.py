import os
import lan
import require_utils
import json


def request_spec(gerrit_account, repo, branch):
    # List of URLs for spec file
    req_url_spec = ['https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/{0}.spec;hb=refs/heads/{1}',
                    'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',
                    'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}']
    idx = 0
    while idx < len(req_url_spec):
        try:
            req_spec = lan.get_requirements_from_url(req_url_spec[idx].format(repo.strip(), branch), gerrit_account)
        except KeyError:
            req_spec = None
        idx += 1
        if req_spec is not None:
            break

    if req_spec is None: 
        try:
            req_url_spec = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;' \
                               'a=blob_plain;f=rpm/SPECS/python-{2}.spec;hb=refs/heads/{1}'.format(repo.strip(), branch, repo.strip().replace('.', '-'))
            req_spec = lan.get_requirements_from_url(req_url_spec, gerrit_account)
        except KeyError:
            print 'Skip ' + repo.strip() + ' RPM repository.'
            req_spec = None

    return req_spec


def request_control(gerrit_account, repo, branch, type):
    # URL for getting changelog file
    req_url_changelog = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;' \
                        'a=blob_plain;f=debian/{2};hb=refs/heads/{1}'.format(repo.strip(), branch, type)

    try:
        req_control = lan.get_requirements_from_url(req_url_changelog, gerrit_account)
    except KeyError:
        print 'Skip ' + repo.strip() + ' DEB repository.'
        req_control = None

    return req_control


def del_symbol(json_file, n):
    json_file.seek(n, os.SEEK_END)
    json_file.truncate()


def get_req(gerritAccount, req_file, rq2, json_file, branch, type):
    pack_count = 0
    repo_count = 0
    for repo in req_file:
        print '\n' * 3, 'Repos:', repo
        req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/{0}.git;' \
                  'a=blob_plain;f=requirements.txt;hb=refs/heads/{1}'.format(repo.strip(), branch)

        # Check the repo is exist. If not - skipping.
        try:
            r = lan.get_requirements_from_url(req_url, gerritAccount)
        except KeyError:
            print 'Skip ' + repo.strip() + ' repository.'
            continue

        rq1 = require_utils.Require(require_utils.Require.parse_req(r))

        if type:

            if type == "control":
                packs_request = request_control(gerritAccount, repo, branch, "control")
            elif type == "spec":
                packs_request = request_spec(gerritAccount, repo, branch)

            with open("{0}-base.json".format(type), 'r') as b:
                base = json.load(b)

            if packs_request is not None:

                if type == "control":
                    packs_list = require_utils.Require.get_packs_control(packs_request)
                    sector = "Depends:"
                elif type == "spec":
                    packs_list = require_utils.Require.get_packs_spec(packs_request)
                    sector = "Requires:"
                    
                for el in packs_list[sector]:
                    if (base.has_key(el)):
                        rq1.packs.setdefault(base[el], list())
                    else:
                        print "Unknown: " + el
            
        if rq1.packs != {}:
            repo_count += 1
            rq = require_utils.Require.merge(rq1.packs, rq2.packs)
            json_file.write('\t{\n' + '\t' * 2 + json.dumps(repo.strip()) + ': {\n')
            json_file.write('\t' * 2 + '"deps": {\n')
            for key in rq1.packs.keys():

                bold_beg = ''
                bold_end = ''

                if require_utils.Require.is_changed(rq[key], rq1.packs[key]):
                    # Write to file with bold font and pointer.
                    pack_count += 1
                    bold_beg = '\033[1m'
                    bold_end = '\033[0m'
                    json_file.write('\t' * 3 + json.dumps(''.join('* ' + '**' + key + '**' + ' ' * 8 )) + ':' +
                                    json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')
                else:
                    # Write to file with standard font.
                    json_file.write('\t' * 3 + json.dumps(''.join(key + ' ' * 8)) + ':' +
                                    json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')

                print '{0}{1}{2}:{3}'.format(bold_beg, key, bold_end, ''.join([" %s%s;" % x for x in rq[key]]))

            # Delete unnecessary comma in the end of dependencies list
            del_symbol(json_file, -2)
            json_file.write('\t' * 2 + '}}},\n')
    if repo_count:
        del_symbol(json_file, -2)
    return pack_count, repo_count


def get_epoch(gerrit_account, req_file, branch, json_file):
    check = False
    for repo in req_file:
        print '\n' * 3, 'Repos:', repo

        req_spec = request_spec(gerrit_account, repo, branch)
        req_control = request_control(gerrit_account, repo, branch, "changelog")

        rpm_epoch = deb_epoch = None

        if req_spec is not None:
            rpm_epoch = require_utils.Require.get_epoch(req_spec)
        if req_control is not None:
            deb_epoch = require_utils.Require.get_epoch(req_control)

        if rpm_epoch or deb_epoch:
            check = True
            json_file.write('\t' * 3 + json.dumps(repo.strip()) + ': {\n')

            if rpm_epoch:
                print "RPM\n" + rpm_epoch + "\n"
                json_file.write('\t' * 4 + '"RPM":' + json.dumps(rpm_epoch) + ',\n')

            if deb_epoch:
                print "DEB\n" + deb_epoch + "\n"
                json_file.write('\t' * 4 + '"DEB":' + json.dumps(deb_epoch) + ',\n')

            del_symbol(json_file, -2)
            json_file.write('\t' * 3 + '},\n')
    if check:
        del_symbol(json_file, -2)