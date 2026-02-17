--Oracle admin details:
--user: 
--passwd: oracle@22

---------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------- Schema and Table space creation ----------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------

----The Below schema is to store the Voting data and user login data in the whole project----
--Schema for storing the tables in the badabase:

sqlplus / as sysdba

ALTER SESSION SET CONTAINER = XEPDB1;

CREATE TABLESPACE secured_voting DATAFILE 'C:\APP\BHARA\PRODUCT\21C\ORADATA\XE\XEPDB1\secured_voting01.dbf' SIZE 100M AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

--User to access the schema
CREATE USER voting_schema IDENTIFIED BY voting123 DEFAULT TABLESPACE secured_voting TEMPORARY TABLESPACE temp QUOTA UNLIMITED ON secured_voting;

--Permission access to users 

GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO voting_schema;


commit;


--CONNECT voting_schema/voting123@XEPDB1


---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------- Table creation -------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------- User details Table creation --------------------------------------------

CREATE SEQUENCE v_user_detail_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE TABLE v_user_detail (
    id           NUMBER
                 DEFAULT v_user_detail_seq.NEXTVAL
                 PRIMARY KEY,
    user_name    VARCHAR2(50) NOT NULL,
    password     VARCHAR2(20) NOT NULL,
    last_login   TIMESTAMP
);

INSERT INTO v_user_detail (user_name, password, last_login) VALUES ('admin', 'admin@123', SYSTIMESTAMP);
INSERT INTO v_user_detail (user_name, password) VALUES ('user_1', 'user@123');

COMMIT;


-------------------------------------------- Voting details Table creation --------------after scan it store----------------------------
CREATE TABLE v_voterid_details(
    voter_id        NUMBER
                    PRIMARY KEY,
    encryption_key  VARCHAR2(256) NOT NULL,
    polling_status  VARCHAR2(20)
                    CHECK (polling_status IN ('NOT_POLLED', 'POLLED')),
    created_on      TIMESTAMP
                    DEFAULT SYSTIMESTAMP
                    NOT NULL,
    polled_on       TIMESTAMP
);
CREATE INDEX v_voting_details_status_idx
ON v_voterid_details (polling_status);
INSERT INTO v_voterid_details(voter_id, encryption_key, polling_status)
VALUES (101, 'A9F3XK29QZ...', 'NOT_POLLED');
COMMIT;

-------------------------------------------voter_prestored_data--------------------------------------------------------------------------
CREATE TABLE v_voterid_prestored_data (
sno NUMBER GENERATED ALWAYS AS IDENTITY,
    voter_id VARCHAR2(50) PRIMARY KEY,
    voter_name varchar2(40), 
    booth_name varchar2(20),
    pincode number
    );
desc v_voterid_prestored_data;

insert into v_voterid_prestored_data (voter_id,voter_name,booth_name,pincode) 
  values ('voter001','votername01','kk nagar',600078);

commit;
--single value update
  
UPDATE v_voterid_prestored_data
SET voter_name = 'shamir'
WHERE voter_id = 'voter002';

commit;
-----------------------------------------------admin table---------------------------------------------------------------------------------------
CREATE SEQUENCE v_admin_detail_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE TABLE v_admin_detail (
    id           NUMBER
                 DEFAULT v_admin_detail_seq.NEXTVAL
                 PRIMARY KEY,
    user_name    VARCHAR2(50) NOT NULL,
    password     VARCHAR2(20) NOT NULL,
    last_login   TIMESTAMP
);

INSERT INTO v_admin_detail (user_name, password, last_login) VALUES ('admin_1', 'admin@123', SYSTIMESTAMP);