
-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding UTF-8

DROP TABLE [tblAgeCategories];
CREATE TABLE [tblAgeCategories]
 (
	[AgeCat]			Text (50)
);

DROP TABLE [tblCamper];
CREATE TABLE [tblCamper]
 (
	[CamperID]			Long Integer, 
	[CamperNum]			Text (100), 
	[RegID]			Long Integer, 
	[PersID]			Long Integer NOT NULL, 
	[CampYear]			Integer NOT NULL, 
	[FtPt]			Text (4) NOT NULL, 
	[ScholarType]			Text (20) NOT NULL, 
	[ScholarReason]			Text (40), 
	[StaffPosition]			Text (100), 
	[HousingAssigned]			Text (20), 
	[Band]			Boolean NOT NULL, 
	[Instruments]			Text (100), 
	[InFamilyProgram]			Boolean NOT NULL, 
	[Flags]			Text (20), 
	[ShirtCut]			Text (2), 
	[ShirtSize]			Text (6), 
	[FreeShirt]			Boolean NOT NULL, 
	[Vegan]			Boolean NOT NULL, 
	[Vegetarian]			Boolean NOT NULL, 
	[DietaryComments]			Text (510), 
	[AlcoholPolicyInitialed]			Boolean NOT NULL, 
	[Notes]			Text (510), 
	[Registered]			Boolean NOT NULL, 
	[CheckedIn]			Boolean NOT NULL
);

DROP TABLE [tblConstantsMembership];
CREATE TABLE [tblConstantsMembership]
 (
	[row]			Long Integer, 
	[CurMemYr]			Integer, 
	[StartDate]			DateTime, 
	[EndDate]			DateTime
);

DROP TABLE [tblDepositOperations];
CREATE TABLE [tblDepositOperations]
 (
	[SavedDepositSlipPDF]			Boolean NOT NULL, 
	[CurrentDepositDate]			DateTime, 
	[Initials]			Text (10)
);

DROP TABLE [tblEmailRegistered];
CREATE TABLE [tblEmailRegistered]
 (
	[LastName]			Text (60), 
	[FirstName]			Text (100), 
	[Expr1]			Text (510)
);

DROP TABLE [tblHelp];
CREATE TABLE [tblHelp]
 (
	[HelpTopic]			Text (200), 
	[HelpText]			OLE (255)
);

DROP TABLE [tblHousingChoices];
CREATE TABLE [tblHousingChoices]
 (
	[Choices]			Text (60) NOT NULL
);

DROP TABLE [tblHousingRooms];
CREATE TABLE [tblHousingRooms]
 (
	[HousingAssigned]			Text (20), 
	[TIFDHousingTypeID]			Text (100)
);

DROP TABLE [tblHousingType];
CREATE TABLE [tblHousingType]
 (
	[TIFDHousingTypeID]			Text (100), 
	[TIFDHousingType]			Text (100), 
	[GFCHousingType]			Text (100)
);

DROP TABLE [tblMembershipType];
CREATE TABLE [tblMembershipType]
 (
	[MemType]			Text (30)
);

DROP TABLE [tblPayments];
CREATE TABLE [tblPayments]
 (
	[PayID]			Long Integer, 
	[MemID]			Long Integer NOT NULL, 
	[RegID]			Long Integer, 
	[ForPerson]			Long Integer, 
	[FromPerson]			Long Integer, 
	[PayType]			Text (12) NOT NULL, 
	[DateRecd]			DateTime NOT NULL, 
	[Cash]			Boolean NOT NULL, 
	[CheckNum]			Text (20), 
	[TotalAmt]			Currency NOT NULL, 
	[PayPalFees]			Currency, 
	[WaitingForDeposit]			Boolean NOT NULL, 
	[WhoHasPossession]			Text (6) NOT NULL, 
	[DepositDate]			DateTime, 
	[MemberFee]			Currency, 
	[NumberYearsPaid]			Byte, 
	[BobbiFund]			Currency, 
	[FloorFund]			Currency, 
	[MusicFund]			Currency, 
	[CampFund]			Currency, 
	[GeneralFund]			Currency, 
	[CampFee]			Currency, 
	[Shirts]			Currency, 
	[Videos]			Currency, 
	[LateFee]			Currency, 
	[HousingFee]			Currency, 
	[TIFDSales]			Currency, 
	[InsuranceFee]			Currency, 
	[Other]			Currency, 
	[ConfirmSent]			Boolean NOT NULL, 
	[Notes]			Text (510)
);

DROP TABLE [tblPerson];
CREATE TABLE [tblPerson]
 (
	[PersID]			Long Integer, 
	[MemID]			Long Integer, 
	[Primary?]			Boolean NOT NULL, 
	[FirstName]			Text (100), 
	[LastName]			Text (60), 
	[AgeCategory]			Text (50) NOT NULL, 
	[Age]			Byte, 
	[DateOfBirth]			DateTime, 
	[Gender]			Text (20), 
	[eMail1]			Text (140), 
	[PubMail1?]			Boolean NOT NULL, 
	[eMail2]			Text (100), 
	[PubMail2?]			Boolean NOT NULL, 
	[WorkCellPhone]			Text (100), 
	[Flags]			Text (100), 
	[Groups]			Text (200), 
	[Notes]			Text (510), 
	[Current]			Boolean NOT NULL
);

DROP TABLE [tblRegForm];
CREATE TABLE [tblRegForm]
 (
	[RegID]			Long Integer, 
	[MemID]			Long Integer NOT NULL, 
	[Year]			Integer NOT NULL, 
	[Postmark]			DateTime, 
	[SecondPage]			Boolean NOT NULL, 
	[ExpLateFee]			Currency, 
	[Received]			DateTime, 
	[RegNum]			Integer, 
	[ConfirmSent]			Boolean NOT NULL, 
	[MobilityAssistanceDevice]			Text (100), 
	[HousingPref]			Text (60), 
	[HousingPref2]			Text (60), 
	[HousingNotes]			Text (510), 
	[QualifyAsFamily]			Boolean NOT NULL, 
	[HousingFee]			Currency, 
	[NumSingers]			Single, 
	[NumSyllabi]			Byte, 
	[ExpCampFees]			Currency, 
	[ExpShirtFees]			Currency, 
	[MembershipRebate]			Currency, 
	[MembershipFee]			Currency, 
	[NumVHS]			Byte, 
	[NumDVD]			Byte, 
	[Adjustment]			Currency NOT NULL, 
	[RefundRequested]			Boolean NOT NULL, 
	[PaymentRequested]			Boolean NOT NULL, 
	[MemYearAtStart]			Long Integer, 
	[Notes]			Text (510)
);

DROP TABLE [tblScholarReason];
CREATE TABLE [tblScholarReason]
 (
	[Reason]			Text (50)
);

DROP TABLE [tblT-shirts];
CREATE TABLE [tblT-shirts]
 (
	[ShirtSize]			Text (6), 
	[NoOfShirts]			Byte, 
	[RegID]			Long Integer, 
	[CampYear]			Integer
);

DROP TABLE [tblConstantsCamp];
CREATE TABLE [tblConstantsCamp]
 (
	[row]			Long Integer, 
	[ThisYear]			Integer, 
	[PrRoomFeeDbl]			Currency, 
	[PrRoomFeeSngl]			Currency, 
	[PrCabinFee]			Currency, 
	[GFCLodgeAdultRate]			Currency, 
	[GFCCabinAdultRate]			Currency, 
	[GFCChildRate]			Currency, 
	[SchFull]			Currency, 
	[SchHalf]			Currency, 
	[SchQuart]			Currency, 
	[AFTFee]			Currency, 
	[APTFee]			Currency, 
	[ANDFee]			Currency, 
	[CFTFee]			Currency, 
	[CPTFee]			Currency, 
	[MemReg]			Currency, 
	[MemFam]			Currency, 
	[LateFee]			Currency, 
	[LateCutoff]			DateTime, 
	[ShirtFee]			Currency, 
	[VideoCost]			Currency, 
	[RegistrarName]			Text (100), 
	[AdultString]			Text (100), 
	[ChildString]			Text (100), 
	[FreeHousingString]			Text (100), 
	[WhoHasPossession]			Text (100)
);

DROP TABLE [tblMemUnit];
CREATE TABLE [tblMemUnit]
 (
	[MemID]			Long Integer, 
	[MailingName]			Text (200), 
	[Address1]			Text (100), 
	[Address2]			Text (100), 
	[City]			Text (60), 
	[State]			Text (20), 
	[Country]			Text (100), 
	[Zip]			Text (40), 
	[HomePhone]			Text (100), 
	[MemberType]			Text (30), 
	[MemberYear]			Integer, 
	[FirstMemberYear]			Integer, 
	[HardCopy?]			Boolean NOT NULL, 
	[FreeNewsletter?]			Boolean NOT NULL, 
	[Notes]			Text (510), 
	[Flags]			Text (20), 
	[LastCampYr]			Integer, 
	[Current]			Boolean NOT NULL
);
