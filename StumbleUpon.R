#read data; parseToWordList; clearBoilerPlate; writeToFileInFormat

#read data
workingDirectory <- 'D:\\Development\\Projects\\SDA\\O-course\\hometask1\\data\\test'
train <- read.table(file.path(workingDirectory, "train.tsv"), sep = "\t", header = TRUE, stringsAsFactors = FALSE)
test <- read.table(file.path(workingDirectory, "test.tsv"), sep = "\t", header = TRUE, stringsAsFactors = FALSE)

library(rjson)
jsonToWordList <- function(json) {
  #requires library rjson
  boilerplate <- unlist(fromJSON(json))
  names(boilerplate) <- NULL
  boilerplate <- paste(boilerplate,collapse=" ")
  boilerplate <- gsub("\\n", "", boilerplate)
  boilerplate <- unlist(strsplit(boilerplate, " "))
  return (boilerplate)
}

clearData = function(data) {
  ret <- list()
  for (text in data) {
    u <- mapply(function(str) { if (nchar(str) <= 2 || str == "the" || nchar(str) > 25) return(FALSE) else return(TRUE)}, text)
    add <- tolower(text[u])
    ret <- append(ret, list(add))
  }
  return(ret)  
}

resultData <- list()
resultTest <- list()

#parseToWordList
#this step will take a while
for(i in 1:length(train$boiler)) {
  resultData <- append(resultData, list(jsonToWordList(train$boiler[i])))
}

for(i in 1:length(test$boiler)) {
  resultTest <- append(resultTest, list(jsonToWordList(test$boiler[i])))
}

#clearing data
#this step also will take a while
resultData <- clearData(resultData)
resultTest <- clearData(resultTest)

writeToFile <- function(filename, data, label = NULL, id = NULL) {
  fileCon <- file(filename)
  open(fileCon, open="w")
  if (!is.null(label)) {
    labels <- as.character(label)
  }
  if (!is.null(id)) {
    ids <- as.character(id)
  }
  for (i in 1 : length(data)) {
    if (!is.null(id)) {
      writeLines(ids[i], fileCon, sep = ' ')
    }
    if (!is.null(label)) {
      writeLines(labels[i], fileCon, sep = ' ')
    }
    writeLines(data[[i]], fileCon, sep = ' ')
    writeLines("", fileCon)
  }  
  close(fileCon)
}

#finally writing files
#format in each line: id label boilerplate
writeToFile(file.path(workingDirectory, "train.txt"), resultData, train$label, train$urlid)
#format in each line: id boilerplate
writeToFile(file.path(workingDirectory, "test.txt"), resultTest, id = test$urlid)
