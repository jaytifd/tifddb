
-- The original schema slightly modified:  some "?" characters were removed from table names
-- and some "NOT NULL" constraints were removed so the table data loaded properly

-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding UTF-8

DROP TABLE IF EXISTS `tblAgeCategories`;
CREATE TABLE `tblAgeCategories`
 (
	`AgeCat`			varchar (50)
);

DROP TABLE IF EXISTS `tblCamper`;
CREATE TABLE `tblCamper`
 (
	`CamperID`			int, 
	`CamperNum`			varchar (100), 
	`RegID`			int, 
	`PersID`			int NOT NULL, 
	`CampYear`			int NOT NULL, 
	`FtPt`			varchar (4) NOT NULL, 
	`ScholarType`			varchar (20) NOT NULL, 
	`ScholarReason`			varchar (40), 
	`StaffPosition`			varchar (100), 
	`HousingAssigned`			varchar (20), 
	`Band`			char NOT NULL, 
	`Instruments`			varchar (100), 
	`InFamilyProgram`			char NOT NULL, 
	`Flags`			varchar (20), 
	`ShirtCut`			varchar (2), 
	`ShirtSize`			varchar (6), 
	`FreeShirt`			char NOT NULL, 
	`Vegan`			char NOT NULL, 
	`Vegetarian`			char NOT NULL, 
	`DietaryComments`			varchar (510), 
	`AlcoholPolicyInitialed`			char NOT NULL, 
	`Notes`			varchar (510), 
	`Registered`			char NOT NULL, 
	`CheckedIn`			char NOT NULL
);

DROP TABLE IF EXISTS `tblConstantsMembership`;
CREATE TABLE `tblConstantsMembership`
 (
	`row`			int, 
	`CurMemYr`			int, 
	`StartDate`			datetime, 
	`EndDate`			datetime
);

DROP TABLE IF EXISTS `tblDepositOperations`;
CREATE TABLE `tblDepositOperations`
 (
	`SavedDepositSlipPDF`			char NOT NULL, 
	`CurrentDepositDate`			date, 
	`Initials`			varchar (10)
);

DROP TABLE IF EXISTS `tblEmailRegistered`;
CREATE TABLE `tblEmailRegistered`
 (
	`LastName`			varchar (60), 
	`FirstName`			varchar (100), 
	`Expr1`			varchar (510)
);

DROP TABLE IF EXISTS `tblHelp`;
CREATE TABLE `tblHelp`
 (
	`HelpTopic`			varchar (200), 
	`HelpText`			varchar (255)
);

DROP TABLE IF EXISTS `tblHousingChoices`;
CREATE TABLE `tblHousingChoices`
 (
	`Choices`			varchar (60) NOT NULL
);

DROP TABLE IF EXISTS `tblHousingRooms`;
CREATE TABLE `tblHousingRooms`
 (
	`HousingAssigned`			varchar (20), 
	`TIFDHousingTypeID`			varchar (100)
);

DROP TABLE IF EXISTS `tblHousingType`;
CREATE TABLE `tblHousingType`
 (
	`TIFDHousingTypeID`			varchar (100), 
	`TIFDHousingType`			varchar (100), 
	`GFCHousingType`			varchar (100)
);

DROP TABLE IF EXISTS `tblMembershipType`;
CREATE TABLE `tblMembershipType`
 (
	`MemType`			varchar (30)
);

DROP TABLE IF EXISTS `tblPayments`;
CREATE TABLE `tblPayments`
 (
	`PayID`			int, 
	`MemID`			int NOT NULL, 
	`RegID`			int, 
	`ForPerson`			int, 
	`FromPerson`			int, 
	`PayType`			varchar (12) NOT NULL, 
	`DateRecd`			date NOT NULL, 
	`Cash`			char NOT NULL, 
	`CheckNum`			varchar (20), 
	`TotalAmt`			float NOT NULL, 
	`PayPalFees`			float, 
	`WaitingForDeposit`			char NOT NULL, 
	`WhoHasPossession`			varchar (6), 
	`DepositDate`			date, 
	`MemberFee`			float, 
	`NumberYearsPaid`			int, 
	`BobbiFund`			float, 
	`FloorFund`			float, 
	`MusicFund`			float, 
	`CampFund`			float, 
	`GeneralFund`			float, 
	`CampFee`			float, 
	`Shirts`			float, 
	`Videos`			float, 
	`LateFee`			float, 
	`HousingFee`			float, 
	`TIFDSales`			float, 
	`InsuranceFee`			float, 
	`Other`			float, 
	`ConfirmSent`			char NOT NULL, 
	`Notes`			varchar (510)
);

DROP TABLE IF EXISTS `tblPerson`;
CREATE TABLE `tblPerson`
 (
	`PersID`			int, 
	`MemID`			int, 
	`Primary?`			char NOT NULL, 
	`FirstName`			varchar (100), 
	`LastName`			varchar (60), 
	`AgeCategory`			varchar (50) NOT NULL, 
	`Age`			int, 
	`DateOfBirth`			date, 
	`Gender`			varchar (20), 
	`eMail1`			varchar (140), 
	`PubMail1?`			char NOT NULL, 
	`eMail2`			varchar (100), 
	`PubMail2?`			char NOT NULL, 
	`WorkCellPhone`			varchar (100), 
	`Flags`			varchar (100), 
	`Groups`			varchar (200), 
	`Notes`			varchar (510), 
	`Current`			char NOT NULL
);

DROP TABLE IF EXISTS `tblRegForm`;
CREATE TABLE `tblRegForm`
 (
	`RegID`			int, 
	`MemID`			int NOT NULL, 
	`Year`			int NOT NULL, 
	`Postmark`			date, 
	`SecondPage`			char NOT NULL, 
	`ExpLateFee`			float, 
	`Received`			date, 
	`RegNum`			int, 
	`ConfirmSent`			char NOT NULL, 
	`MobilityAssistanceDevice`			varchar (100), 
	`HousingPref`			varchar (60), 
	`HousingPref2`			varchar (60), 
	`HousingNotes`			varchar (510), 
	`QualifyAsFamily`			char NOT NULL, 
	`HousingFee`			float, 
	`NumSingers`			float, 
	`NumSyllabi`			int, 
	`ExpCampFees`			float, 
	`ExpShirtFees`			float, 
	`MembershipRebate`			float, 
	`MembershipFee`			float, 
	`NumVHS`			int, 
	`NumDVD`			int, 
	`Adjustment`			float NOT NULL, 
	`RefundRequested`			char NOT NULL, 
	`PaymentRequested`			char NOT NULL, 
	`MemYearAtStart`			int, 
	`Notes`			varchar (510)
);

DROP TABLE IF EXISTS `tblScholarReason`;
CREATE TABLE `tblScholarReason`
 (
	`Reason`			varchar (50)
);

DROP TABLE IF EXISTS `tblT-shirts`;
CREATE TABLE `tblT-shirts`
 (
	`ShirtSize`			varchar (6), 
	`NoOfShirts`			int, 
	`RegID`			int, 
	`CampYear`			int
);

DROP TABLE IF EXISTS `tblConstantsCamp`;
CREATE TABLE `tblConstantsCamp`
 (
	`row`			int, 
	`ThisYear`			int, 
	`PrRoomFeeDbl`			float, 
	`PrRoomFeeSngl`			float, 
	`PrCabinFee`			float, 
	`GFCLodgeAdultRate`			float, 
	`GFCCabinAdultRate`			float, 
	`GFCChildRate`			float, 
	`SchFull`			float, 
	`SchHalf`			float, 
	`SchQuart`			float, 
	`AFTFee`			float, 
	`APTFee`			float, 
	`ANDFee`			float, 
	`CFTFee`			float, 
	`CPTFee`			float, 
	`MemReg`			float, 
	`MemFam`			float, 
	`LateFee`			float, 
	`LateCutoff`			datetime, 
	`ShirtFee`			float, 
	`VideoCost`			float, 
	`RegistrarName`			varchar (100), 
	`AdultString`			varchar (100), 
	`ChildString`			varchar (100), 
	`FreeHousingString`			varchar (100), 
	`WhoHasPossession`			varchar (100)
);

DROP TABLE IF EXISTS `tblMemUnit`;
CREATE TABLE `tblMemUnit`
 (
	`MemID`			int, 
	`MailingName`			varchar (200), 
	`Address1`			varchar (100), 
	`Address2`			varchar (100), 
	`City`			varchar (60), 
	`State`			varchar (20), 
	`Country`			varchar (100), 
	`Zip`			varchar (40), 
	`HomePhone`			varchar (100), 
	`MemberType`			varchar (30), 
	`MemberYear`			int, 
	`FirstMemberYear`			int, 
	`HardCopy?`			char NOT NULL, 
	`FreeNewsletter?`			char NOT NULL, 
	`Notes`			varchar (510), 
	`Flags`			varchar (20), 
	`LastCampYr`			int, 
	`Current`			char NOT NULL
);
