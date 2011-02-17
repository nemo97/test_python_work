'''
Created on Feb 15, 2011

@author: Subhas
'''
import fileinput
import operator

class Config:
    to_year =0
    from_year =0
#   will take maximum number of count for analysis , required for testing
    fltCount =0
#    required for Devisible by predefined number criteria
    preDefinedDivident = 0
    def __init__(self):
        self.to_year = 2011
        self.from_year=2010
        self.fltCount =10
        self.preDefinedDivident=10

class MileageDTO:
    accountNbr=0
    fltNbr=0
    flExpCcYy=0
    mileageType ="" # E1,E2,A,N
    juris= "" # AL,AR,....
    mileage = 0 # Mileage q
    mileagePerc = 0.0 # Mileage q

    def display(self):
        strval = ":"+str(self.accountNbr)+str(self.fltNbr)+str(self.flExpCcYy)+self.juris+" Mileage Type : "+ self.mileageType + " Mileage : "+ str(self.mileage)
        return strval

    def __str__(self):
        return self.display()

    def __eq__(self,other):
        return self.accountNbr == other.accountNbr and self.fltNbr==other.fltNbr and self.flExpCcYy==other.flExpCcYy


class CriteriaDTO:
    id = 0
    name = "" # hold the criteria name
    weight = 0

    def display(self):
        strval = " Name : "+ self.name +" Weight : "+ str(self.weight) + " id : "+ str(self.id)
        return strval

    def __str__(self):
        return self.display()

class InitDataPopulationClass:
#LAYOUT
#SELECT MCS_IR_MLG.ACCOUNT_NBR, MCS_IR_MLG.FL_NBR, MCS_IR_MLG.FL_EXP_CCYY, MCS_IR_MLG.JUR, MCS_IR_MLG.MLG, MCS_IR_MLG.PERCENT, MCS_IR_MLG.MLG_TYPE_IND FROM DB2ADMIN.MCS_IR_MLG AS MCS_IR_MLG
#WHERE MCS_IR_MLG.FL_EXP_CCYY in  (2012,2011,2010,2009)

    dataList = []
    #criteriaList = []
    config = Config()

    # required for Identical Actual Distance
    infoLatestActualIdenticalDistance = []
    infoPreviousActualIdenticalDistance =[]
    maximumExposureActualIdenticalDistance = 0;

    # required for identical estimated mileage

    infoLatestEstimatedIdenticalDistance = []
    infoPreviousEstimatedIdenticalDistance = []
    maximumExposureEstimatedIdenticalDistance = 0

    # required for divisible by predefined number
    infoLatestDivisibleMileageDistance = []
    infoPreviousDivisibleMileageDistance = []
    maximumExposureDivisibleMileageDistance = 0

    # required for identical percentage
    infoLatestIdenticalPercentageDistance = []
    infoPreviousIdenticalPercentageDistance = []
    maximumExposureIdenticalPercentageDistance = 0

    def __init__(self):
#        x = MileageDTO()
#        x.juris = "AL"
#        x.mileageYear = 2010
#        x.mileage = 100
#        x.weight = "A"
#        self.dataList.append(x);
#
#        x = MileageDTO()
#        x.juris = "AL"
#        x.mileageYear = 2009
#        x.mileage = 100
#        x.weight = "A"
#        self.dataList.append(x);
        #linestring = open('mileagedata.txt', 'r').read()
        #lines = linestring.split('\n')
        config = Config()
        self.config = config;
        #for i,v in enumerate(lines):
#	for v in open('mileagedata.txt', 'r'):
        for v in fileinput.input('mileagedata.txt'):
            x = MileageDTO()
            strLineToken = v.split(',');
#            print strLineToken
            if(len(strLineToken) == 7):
#                print strLineToken
                if((int(strLineToken[2]) < int(config.from_year)) or (int(strLineToken[2]) > int(config.to_year))): continue

                x.accountNbr = strLineToken[0];
                x.fltNbr = strLineToken[1];
                x.flExpCcYy = strLineToken[2];
                x.juris = strLineToken[3].strip(' \t\n\r\"\''); # remove " from Db2 data
                x.mileage = strLineToken[4];
                x.mileagePerc = strLineToken[5];
                x.mileageType =strLineToken[6].strip(' \t\n\r\"\'');
                self.dataList.append(x);

#        print self.dataList
        # load criteria configuration
        print "File Read Completed.."


    def getMileageDataFor(self,accountNbr,fltNbr,fltExpCcYy):
        tempList = [];
        for i,v in enumerate(self.dataList) :
            if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType=="A")):
                tempList.append(v)

        return tempList;

    def getDistinctFleets(self,year):
        tempList = [];
        for i,v in enumerate(self.dataList) :
            if((int(v.flExpCcYy) == int(year)) & (v not in tempList)):
                tempList.append(v)

            if(len(tempList) > config.fltCount): break;



        return tempList;

    def getExposureForIdenticalActual(self,accountNbr,fltNbr,fltExpCcYy):
        count = 0
        for i,v in enumerate(self.dataList) :
            # and v.mileageType=="A" and v.accountNbr==accountNbr and v.fltNbr==fltNbr
            if((int(v.accountNbr)==int(accountNbr)) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType=="A")):
                count += 1;

        return count;

    def processAndPoulateDataForEveryCriteria(self,accountNbr,fltNbr,fltExpCcYy,criteriaDTO):

    	previousYear = int(fltExpCcYy)-1;
#var for identical actual mileage
        infoLatestActualIdenticalDistanceLocal = []
        infoPreviousActualIdenticalDistanceLocal =[]
        maximumExposureActualIdenticalDistanceLocal = 0

#var for identical estimated mileage
        infoLatestEstimatedIdenticalDistanceLocal = []
        infoPreviousEstimatedIdenticalDistanceLocal =[]
        maximumExposureEstimatedIdenticalDistanceLocal = 0

#var for divisible mileage criteria
        infoLatestDivisibleMileageDistanceLocal = []
        infoPreviousDivisibleMileageDistanceLocal =[]
        maximumExposureDivisibleMileageDistanceLocal = 0

#var for identical percentage criteria
        infoLatestIdenticalPercentageDistanceLocal = []
        infoPreviousIdenticalPercentageDistanceLocal =[]
        maximumExposureIdenticalPercentageDistanceLocal = 0

    	for i,v in enumerate(self.dataList) :

    	   if(criteriaDTO.name=='IdenticalActualMileage'):

    		   if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType=="A") &(float(v.mileage) >0)):
    			infoLatestActualIdenticalDistanceLocal.append(v)

    		   if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(previousYear)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType=="A")&(float(v.mileage) >0)):
    			infoPreviousActualIdenticalDistanceLocal.append(v)

    		   if((int(v.accountNbr)==int(accountNbr)) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType=="A")&(float(v.mileage) >0)):
    			maximumExposureActualIdenticalDistanceLocal += 1;

           if(criteriaDTO.name=='IdenticalEstimationMileage'):
               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType in ("E1","E2"))):
                infoLatestEstimatedIdenticalDistanceLocal.append(v)

               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(previousYear)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType in ("E1","E2"))):
                infoPreviousEstimatedIdenticalDistanceLocal.append(v)

               if((int(v.accountNbr)==int(accountNbr)) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (v.mileageType in ("E1","E2"))):
                maximumExposureEstimatedIdenticalDistanceLocal += 1;

           if(criteriaDTO.name=='DivisibleMileage'):
               reminder = float(v.mileage) % self.config.preDefinedDivident
               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (reminder==0)):
                infoLatestDivisibleMileageDistanceLocal.append(v)

               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(previousYear)) & (int(v.fltNbr) == int(fltNbr)) & (reminder==0)):
                infoPreviousDivisibleMileageDistanceLocal.append(v)

               if((int(v.accountNbr)==int(accountNbr)) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr)) & (reminder==0)):
                maximumExposureDivisibleMileageDistanceLocal += 1;

           if(criteriaDTO.name=='IdenticalPercentage'):
               mileagePerc = float(v.mileagePerc)

               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr))& (mileagePerc >0)):
                infoLatestIdenticalPercentageDistanceLocal.append(v)

               if((v.accountNbr==accountNbr) & (int(v.flExpCcYy) == int(previousYear)) & (int(v.fltNbr) == int(fltNbr))& (mileagePerc >0)):
                infoPreviousIdenticalPercentageDistanceLocal.append(v)

               if((int(v.accountNbr)==int(accountNbr)) & (int(v.flExpCcYy) == int(fltExpCcYy)) & (int(v.fltNbr) == int(fltNbr))& (mileagePerc >0)):
                maximumExposureIdenticalPercentageDistanceLocal += 1;

        self.infoLatestActualIdenticalDistance = infoLatestActualIdenticalDistanceLocal
        self.infoPreviousActualIdenticalDistance = infoPreviousActualIdenticalDistanceLocal
        self.maximumExposureActualIdenticalDistance = maximumExposureActualIdenticalDistanceLocal

        self.infoLatestEstimatedIdenticalDistance = infoLatestEstimatedIdenticalDistanceLocal
        self.infoPreviousEstimatedIdenticalDistance = infoPreviousEstimatedIdenticalDistanceLocal
        self.maximumExposureEstimatedIdenticalDistance = maximumExposureEstimatedIdenticalDistanceLocal

        self.infoLatestDivisibleMileageDistance = infoLatestDivisibleMileageDistanceLocal
        self.infoPreviousDivisibleMileageDistance = infoPreviousDivisibleMileageDistanceLocal
        self.maximumExposureDivisibleMileageDistance = maximumExposureDivisibleMileageDistanceLocal

        self.infoLatestIdenticalPercentageDistance = infoLatestIdenticalPercentageDistanceLocal
        self.infoPreviousIdenticalPercentageDistance = infoPreviousIdenticalPercentageDistanceLocal
        self.maximumExposureIdenticalPercentageDistance = maximumExposureIdenticalPercentageDistanceLocal

#    Return no of occourance for fleet
    def getMatchingJurisWithPreviousYearIdenticalActual(self,accountNbr,fltNbr,fltExpCcYy):

#        print "Maximum Exposure ",maximumExposure,accountNbr, fltNbr, fltExpCcYy

        count =0;
#        if(len(self.infoPreviousActualIdenticalDistance)==0 or len(self.infoLatestActualIdenticalDistance)==0):
#        	print "no data has been populated",accountNbr, fltNbr, fltExpCcYy

        for prevousElement in  self.infoPreviousActualIdenticalDistance:
#            print "prvious ",prevousElement
            for i,v in enumerate(self.infoLatestActualIdenticalDistance) :
#                print "new " ,v.display()
                if((v.accountNbr==prevousElement.accountNbr) & (int(v.fltNbr) == int(prevousElement.fltNbr)) & (v.juris == prevousElement.juris) &(float(v.mileage) == float(prevousElement.mileage))):
                    count += 1;

#        if(count > 0):
#                print "Identical Juris",maximumExposure,count,v.accountNbr, v.fltNbr, fltExpCcYy

        return count;

#    Return no of occourance for fleet
    def getMatchingJurisWithPreviousYearIdenticalEstimation(self,accountNbr,fltNbr,fltExpCcYy):

        count =0;
#        if(len(self.infoPreviousActualIdenticalDistance)==0 or len(self.infoLatestActualIdenticalDistance)==0):
#            print "no data has been populated",accountNbr, fltNbr, fltExpCcYy

        for prevousElement in  self.infoPreviousEstimatedIdenticalDistance:
#            print "prvious ",prevousElement
            for i,v in enumerate(self.infoLatestEstimatedIdenticalDistance) :
#                print "new " ,v.display()
                if((v.accountNbr==prevousElement.accountNbr) & (int(v.fltNbr) == int(prevousElement.fltNbr)) & (v.juris == prevousElement.juris) &(float(v.mileage) == float(prevousElement.mileage))):
                    count += 1;

#        if(count > 0):
#                print "Identical Juris",maximumExposure,count,v.accountNbr, v.fltNbr, fltExpCcYy

        return count;

#    Return no of occourance for fleet
    def getMatchingJurisWithPreviousYearDivisibleMileage(self,accountNbr,fltNbr,fltExpCcYy):

        count =0;
#        if(len(self.infoPreviousActualIdenticalDistance)==0 or len(self.infoLatestActualIdenticalDistance)==0):
#            print "no data has been populated",accountNbr, fltNbr, fltExpCcYy

        for prevousElement in  self.infoPreviousDivisibleMileageDistance:
#            print "prvious ",prevousElement
            for i,v in enumerate(self.infoLatestDivisibleMileageDistance) :
#                print "new " ,v.display()
                if((v.accountNbr==prevousElement.accountNbr) & (int(v.fltNbr) == int(prevousElement.fltNbr)) & (v.juris == prevousElement.juris)):
                    count += 1;

#        if(count > 0):
#                print "Identical Juris",maximumExposure,count,v.accountNbr, v.fltNbr, fltExpCcYy

        return count;

#    Return no of occourance for fleet
    def getMatchingJurisWithPreviousYearIdenticalPercentage(self,accountNbr,fltNbr,fltExpCcYy):

        count =0;
#        if(len(self.infoPreviousActualIdenticalDistance)==0 or len(self.infoLatestActualIdenticalDistance)==0):
#            print "no data has been populated",accountNbr, fltNbr, fltExpCcYy

        for prevousElement in  self.infoPreviousIdenticalPercentageDistance:
#            print "prvious ",prevousElement
            for i,v in enumerate(self.infoLatestIdenticalPercentageDistance) :
#                print "new " ,v
                if((v.accountNbr==prevousElement.accountNbr) & (int(v.fltNbr) == int(prevousElement.fltNbr)) & (v.juris == prevousElement.juris)& (float(v.mileagePerc)> 0) &(float(v.mileagePerc) == float(prevousElement.mileagePerc))):
                    count += 1;

        if(count > 0):
                print "Identical Perc ",count,v.accountNbr, v.fltNbr, fltExpCcYy

        return count;

# global
x = InitDataPopulationClass();
config = Config()

def calculate(criteriaList):
    to_year = config.to_year
    from_year = config.from_year

    globalMap ={}
    globalMapFinal ={}
    while(to_year > from_year):
        distinctFleets = x.getDistinctFleets(to_year);

        print "Distinct fleet Completed "


        for criteriaElement in criteriaList:
        # iterate over all criteria
            for i,v in enumerate(distinctFleets):
            # start fleet lloping
            	unWeightPoint= 0
                weightPoint = 0;
                weight = criteriaElement.weight
                # load data for all criteria ... as loading for every criteria was so slow
            	x.processAndPoulateDataForEveryCriteria(v.accountNbr, v.fltNbr, to_year,criteriaElement)

            	if(criteriaElement.name=='IdenticalActualMileage'):
                    noOfocourance = x.getMatchingJurisWithPreviousYearIdenticalActual(v.accountNbr, v.fltNbr, to_year);
                    if(x.maximumExposureActualIdenticalDistance >0):
                       unWeightPoint = float(noOfocourance) / float(x.maximumExposureActualIdenticalDistance);
                    else:
                        unWeightPoint=0;

                if(criteriaElement.name=='IdenticalEstimationMileage'):
                    noOfocourance = x.getMatchingJurisWithPreviousYearIdenticalEstimation(v.accountNbr, v.fltNbr, to_year);
                    if(x.maximumExposureEstimatedIdenticalDistance >0):
                       unWeightPoint = float(noOfocourance) / float(x.maximumExposureEstimatedIdenticalDistance);
                    else:
                        unWeightPoint=0;

                if(criteriaElement.name=='DivisibleMileage'):
                    noOfocourance = x.getMatchingJurisWithPreviousYearDivisibleMileage(v.accountNbr, v.fltNbr, to_year);
                    if(x.maximumExposureDivisibleMileageDistance >0):
                       unWeightPoint = float(noOfocourance) / float(x.maximumExposureDivisibleMileageDistance);
                    else:
                        unWeightPoint=0;

                if(criteriaElement.name=='IdenticalPercentage'):
                    noOfocourance = x.getMatchingJurisWithPreviousYearIdenticalPercentage(v.accountNbr, v.fltNbr, to_year);
                    if(x.maximumExposureIdenticalPercentageDistance >0):
                       unWeightPoint = float(noOfocourance) / float(x.maximumExposureIdenticalPercentageDistance);
                    else:
                        unWeightPoint=0;

                if(unWeightPoint > 0):
                    mapKey = str(v.accountNbr)+str(to_year)+str(v.fltNbr)
                    if mapKey in globalMap:
                        globalMap[mapKey] = float(globalMap[mapKey]) + unWeightPoint
                        globalMapFinal[mapKey] = float(globalMapFinal[mapKey]) + float(unWeightPoint)*float(weight)
                    else:
                        globalMap[mapKey] = unWeightPoint
                        globalMapFinal[mapKey] = float(unWeightPoint)*float(weight)

           # end of fleet looping
        to_year = to_year -1;
        #end of

        sorted_x = sorted(globalMap.iteritems(), key=operator.itemgetter(1),reverse=True)
        sorted_final = sorted(globalMapFinal.iteritems(), key=operator.itemgetter(1),reverse=True)
        print "Unweighted Result"+str(sorted_x)
        print "Final Result"+str(sorted_final)

def main():

   while(True):
        option = raw_input('\n\n\nSelect operation : 1- Do again,2- exit ')
        option = option.strip(' \t\n\r\"\'')
        if(option in ['1']):
                criteriaList = [];
                print "\nPlease enter weight for various criteria (enter nothing will be omitted)"
                identicalCriteria = raw_input('Weight (Identical Actual Mileage)  : ->')
                identicalCriteria = identicalCriteria.strip(' \t\n\r\"\'')
                if(identicalCriteria != ''):
                    identicalCriteriaDTO = CriteriaDTO()
                    identicalCriteriaDTO.id = 1;
                    identicalCriteriaDTO.name = 'IdenticalActualMileage'
                    identicalCriteriaDTO.weight = float(identicalCriteria);
                    criteriaList.append(identicalCriteriaDTO);

                identicalEstimationCriteria = raw_input('Wight (Identical estimated distance) : ->')
                identicalEstimationCriteria = identicalEstimationCriteria.strip(' \t\n\r\"\'')
                if(identicalEstimationCriteria != ''):
                    identicalEstimationCriteriaDTO = CriteriaDTO()
                    identicalEstimationCriteriaDTO.id = 2;
                    identicalEstimationCriteriaDTO.name = 'IdenticalEstimationMileage'
                    identicalEstimationCriteriaDTO.weight = float(identicalEstimationCriteria);
                    criteriaList.append(identicalEstimationCriteriaDTO);

                identicalPercentageCriteria = raw_input('Wight (Identical Percentage) : ->')
                identicalPercentageCriteria = identicalPercentageCriteria.strip(' \t\n\r\"\'')
                if(identicalPercentageCriteria != ''):
                    identicalPercentageCriteriaDTO = CriteriaDTO()
                    identicalPercentageCriteriaDTO.id = 4;
                    identicalPercentageCriteriaDTO.name = 'IdenticalPercentage'
                    identicalPercentageCriteriaDTO.weight = float(identicalPercentageCriteria);
                    criteriaList.append(identicalPercentageCriteriaDTO);

                divisibleMileaseCriteria = raw_input('Wight (Mileage divisible by predefined number) : ->')
                divisibleMileaseCriteria = divisibleMileaseCriteria.strip(' \t\n\r\"\'')
                if(divisibleMileaseCriteria != ''):
                    divisibleMileaseCriteriaDTO = CriteriaDTO()
                    divisibleMileaseCriteriaDTO.id = 3;
                    divisibleMileaseCriteriaDTO.name = 'DivisibleMileage'
                    divisibleMileaseCriteriaDTO.weight = float(divisibleMileaseCriteria);
                    criteriaList.append(divisibleMileaseCriteriaDTO);



                if(len(criteriaList)==0):
                    print "No criteria has been entered"
                else:
                    calculate(criteriaList)

        elif(option in ['2']):
        	  break;

        else:
            continue




#    for i,v in enumerate(x.getMileageDataFor(2010, 'AL')) :
#        print i,v.display()



if __name__ == '__main__':
    main();

