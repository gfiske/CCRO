#QuashnetDataRetrieval.R
#collects historic discharge data from the USGS gauging station on the Quashnet River in Massachusetts
#CCRO project
#October 3, 2017
#reference: https://owi.usgs.gov/R/dataRetrieval.html

#install package
##install.packages (c("dataRetrieval","EGRET"))

#load library
rm(list = ls())
library(EGRET)

#retrieve daily dishcarge data for the Quashnet
siteNumber <- "011058837"
QParameterCd <- "00060"
StartDate <- "2016-05-01"
EndDate <- "2017-03-19"
Daily <- readNWISDaily(siteNumber, QParameterCd, StartDate, EndDate)

#install packages
##install.packages("zoo")
##install.packages("dataRetrieval")

#load library
rm(list = ls())
library(dataRetrieval)
library(ggplot2)

#retrieve all dishcarge data for the Quashnet
siteNumber <- "011058837"
parameterCd <- "00060" # Discharge (cfs)
startDate <- "2016-05-01"
endDate <- "2017-03-19"
dischargeAll <- readNWISuv(siteNumber, parameterCd,
                                       startDate, endDate)

#correct the column names
names(dischargeAll)
dischargeAll <- renameNWISColumns(dischargeAll)
names(dischargeAll)

#plot the data
ts <- ggplot(data = dischargeAll, aes(dateTime,Flow_Inst)) + geom_line()
parameterInfo <- attr(dischargeAll, "variableInfo")
siteInfo <- attr(dischargeAll, "siteInfo")

ts <- ts + xlab("") +
  ylab(parameterInfo$parameter_desc) +
  ggtitle(siteInfo$station_nm)
ts

# Write output to CSV
write.csv(dischargeAll, file = "C:/Data/Crap/QuashnetDischarge.csv",row.names=FALSE)
  

