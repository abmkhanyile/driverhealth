from tokenize import Number
import dhclients
from user_accounts.models import CustomUser
from dhclients.models import DHClient, ClientDocument
from datetime import datetime, tzinfo
from countries.models import Country
from django.db.utils import IntegrityError, DatabaseError
from django.conf import settings
import pytz
from django.core.exceptions import ObjectDoesNotExist

class CreateNewUsers:
    def action(self):
        # user_strings = None
        # userprof_strings = None
        # with open('miscellaneous/users_customuser.csv', mode='r') as f:
        #     user_strings = f.readlines()[1:]
            
        # with open('miscellaneous/users_driverprofile.csv', mode='r') as f2:
        #     userprof_strings = f2.readlines()[1:]
        
        # for userstr in user_strings:
        #     userarr = userstr.split(',')
        #     if userarr[17] == 'True':
        #         for userprof in userprof_strings:
        #             userprofarr = userprof.split(',')
        #             if userarr[0].strip() == userprofarr[0].strip():
        #                 try:
        #                     # print(self.ret_proper_date(userarr[2].strip('""')))
        #                     driver =  CustomUser.objects.create(                    
        #                         password = userarr[1].strip('""'),
        #                         last_login = self.ret_proper_date(userarr[2].strip('""')),
        #                         is_superuser = self.convert_bools(userarr[3].strip('""')),
        #                         first_name = userarr[4].strip('""'),
        #                         last_name = userarr[5].strip('""'),
        #                         is_staff = self.convert_bools(userarr[6].strip('""')),
        #                         date_joined = self.ret_proper_date(userarr[7].strip('""')),
        #                         email = userarr[8].strip('""'),
        #                         username = userarr[9].strip('""'),
        #                         contactNumber = userarr[11].strip('""'),
        #                         is_active = self.convert_bools(userarr[12].strip('""')),
        #                         dh_id = userarr[14].strip('""'),
        #                         terms = True
        #                     )
                            
        #                     driverprofile = DHClient.objects.create(
        #                         user = driver,
        #                         nationality = self.match_counrty(userprofarr[3].strip('""')),
        #                         has_passport = self.convert_bools(userprofarr[14].strip('""')),
        #                         passport_num = self.ret_passport_num(userprofarr[6].strip('""')),
        #                         crossborder = self.convert_bools(userprofarr[13].strip('""')),
        #                         rating = int(userprofarr[9].strip('""')),
        #                         dh_test_comment = userprofarr[10].strip('""'),
        #                         tested = self.convert_bools(userprofarr[11].strip('""')),
        #                         in_job_market = self.convert_bools(userprofarr[12].strip('""')),
        #                         profile_picture = self.fix_pic_url(userprofarr[7].strip('""')),
        #                         date_created = self.ret_proper_date(userprofarr[8].strip('""'))
        #                     )
        #                 except DatabaseError as e:
        #                     print(e)
        #                     continue

        user_strings = None
        userprof_strings = None
        with open('miscellaneous/users_customuser.csv', mode='r') as f:
            user_strings = f.readlines()[1:]

        doc_strings = None
        with open('miscellaneous/driver_driverdocument.csv', mode='r') as f:
            doc_strings = f.readlines()[1:]

             
        for userstr in user_strings:
            userarr = userstr.split(',')
            if userarr[17] == 'True':
                for docstr in doc_strings:
                    doc_arr = docstr.split(',')
                    
                    if userarr[0].strip() == doc_arr[3].strip():
                        driver = CustomUser.objects.get(username=userarr[9].strip('""'))
                   
                        dhclient = None
                        try:
                            dhclient = driver.dhclient
                            vis = None

                            try:
                                vis = self.ref_doc_visibility(int(doc_arr[7].strip('""')))
                            except ValueError as c:
                                vis = 1
                                continue

                            try:
                                ClientDocument.objects.create(
                                    client = dhclient,
                                    document = self.fix_pic_url(doc_arr[1].strip('""')),
                                    doc_type = int(doc_arr[4].strip('""')),
                                    doc_visibility = vis,
                                    other_type = doc_arr[5].strip('""'),
                                    doc_name = doc_arr[6].strip('""'),
                                    creation_date = self.ret_proper_date(doc_arr[2].strip('""'))
                                )
                            except DatabaseError as e:
                                print(e)
                                continue
                            
                        except ObjectDoesNotExist as e:
                            print(e)
                            continue
                        
                       

        

        


    def convert_bools(self, bool):
        if bool == "True":
            return True
        elif bool == "False":
            return False
        else:
            return None

    def match_counrty(self, c_id):
        files_countries = {
            '1': 'South Africa',
            '2': 'Botswana',
            '3': 'Eswatini',
            '4': 'Namibia',
            '5': 'Malawi',
            '6': 'Mozambique',
            '7': 'Lesotho',
            '8': 'Zambia',
            '9': 'Zimbabwe',
            '10': 'DRC',
            '11': 'Tanzania',
        }
        return Country.objects.get(long_name=files_countries[c_id])


    def ret_passport_num(self, num):
        if num != "NULL":
            return num
        else:
            return ""

    def fix_pic_url(self, url):
        fixed_url = url.replace("Driver_Documents", "Client_Documents")
        return fixed_url

    def ret_proper_date(self, date_str):
        if date_str == "NULL":
            return None
        else:
            date = datetime.strptime(date_str[0:19], '%Y-%m-%d %H:%M:%S')
            return date.replace(tzinfo=pytz.UTC)


    def ref_doc_visibility(self, vis):
        if isinstance(vis, int):
            print(vis)
            return vis
        else:
            print("else aprt ", vis)
            return 1



                
