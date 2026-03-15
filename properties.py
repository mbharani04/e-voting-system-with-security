#Database connection
DB_USER = "voting_schema"
DB_PASS = "voting123"
DSN = "localhost:1521/XEPDB1"

#User login Query
get_user = """
                SELECT user_name
                FROM v_user_detail
                WHERE user_name = :uname
                  AND password = :pwd
            """
#User last login update query
update_user_lastlogin = """
                    UPDATE v_user_detail
                    SET last_login = SYSTIMESTAMP
                    WHERE user_name = :uname
                """
#Get voter id details from Database
get_voter_details = """
                    select voter_id, voter_name,booth_name,POLLED_STATUS
                    from V_VOTERID_DETAILS
                    where voter_id = :voterId
                """

#Update voter details
# insert_voter_id = """Insert V_VOTERID_DETAILS(voter_id) valuse(:voter_id)"""

update_qr_status = """ 
                    update V_VOTERID_DETAILS 
                    set qr_status = 'Y',
                    qr_dttm = SYSTIMESTAMP
                    where voter_id = :voter_Id
"""