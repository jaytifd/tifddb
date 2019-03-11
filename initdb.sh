dbname="tifd"
mdbfile="TIFD_DB_2019-03-01.mdb"

#an edited schema of the tifd db - remove some "?" from table names, remove some table contraints, etc.
schema="newschema.edited"

mysql -e "drop database $dbname"
mysql -e "create database tifd"
#mdb-schema --drop-table TIFD_DB.mdb mysql | grep -v COMMENT | mysql $dbname
cat $schema | mysql $dbname

tables=`mdb-schema --drop-table $mdbfile mysql | grep -v COMMENT | grep -v tblHelp | grep CREATE | cut -f2 -d\\\``

for table in $tables
	do
	echo -n importing $table.. 
	mdb-export -D '%Y-%m-%d' -I mysql $mdbfile $table| mysql -f $dbname	
	echo return code: $?
	done

echo  "alter table tblPerson add index persID (persID)" | mysql $dbname
echo  "alter table tblCamper add index persID (persID)" | mysql $dbname

#remove the silly "tbl" prefix and the CamelCase
#and re-name the indexes sensibly so that symfony can use them without trouble


IFS='
'

lines="rename table tblAgeCategories to agecategories;
rename table tblConstantsCamp to constantscamp;
rename table tblConstantsMembership to constantsmembership;
rename table tblHelp to help;
rename table tblHousingChoices to housingchoices;
rename table tblHousingRooms to housingrooms;
rename table tblHousingType to housingtype;
rename table \`tblT-shirts\` to tshirts;

rename table tblEmailRegistered to emailregistered;
rename table tblMembershipType to membershiptype;
rename table tblScholarReason to scholarreason;

rename table tblDepositOperations to depositoperations;
rename table tblPayments to payments;

rename table tblCamper to camper;
rename table tblMemUnit to memunit;
rename table tblPerson to person;
rename table tblRegForm to regform;

ALTER TABLE camper CHANGE CamperID id int ;
ALTER TABLE camper CHANGE RegID regform_id int ;
ALTER TABLE camper CHANGE PersID person_id int ;

ALTER TABLE memunit CHANGE MemID id int ;

ALTER TABLE person CHANGE PersID id int ;
ALTER TABLE person CHANGE MemID memunit_id int ;

ALTER TABLE regform CHANGE RegID id int ;
ALTER TABLE regform CHANGE MemID memunit_id int ;
"
for l in $lines
do
echo "$l"
echo $l | mysql $dbname

done

#" | mysql $dbname

