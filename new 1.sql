en phone amma kita iruku phone pesitu irukagaok ok

okok

nan ipo ena pandrana voter detils la table la podran


ok ah


CREATE TABLE v_voterid_details(
    voter_id        VARCHAR2(16)
                    PRIMARY KEY,
    encryption_key  VARCHAR2(256) NOT NULL,
    qr_status  VARCHAR2(1) not NULL,
	polling_status  VARCHAR2(1) not NULL,
    created_on      TIMESTAMP
    polled_on       TIMESTAMP
);


Intha table la party details name and ethana vote nu potuvechikalm   sql la paruga votinschema 2 create agiiruku melaa ama
athu 2 times open pana apadi dhn varum
no andhamari ilaa mela votingschema1.sql apidi iruku paruga kaatu enga


CREATE SEQUENCE v_party_detail_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE TABLE v_party_detail (
    id           NUMBER
                 DEFAULT v_user_detail_seq.NEXTVAL
                 PRIMARY KEY,
    party_name    VARCHAR2(150) NOT NULL,
    party_code    VARCHAR2(6) NOT NULL,
    polled_count  NUMBER 
);

INSERT into v_party_detail values('JJP','002011',0);
INSERT into v_party_detail values('BMK','002012',0);
INSERT into v_party_detail values('MBK','002013',0);

trunc panradhuku munadi backup vachikalamla